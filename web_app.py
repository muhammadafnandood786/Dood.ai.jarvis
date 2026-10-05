#!/usr/bin/env python3
"""
JARVIS Web Interface - Vercel compatible
Works on Mobile, PC, Laptop browsers.
"""

import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

# Make paths work both locally and on Vercel
BASE_DIR = Path(__file__).resolve().parent

from modules.ai_brain import AIBrain
from modules.commands import CommandHandler

app = FastAPI(title="JARVIS AI Assistant", version="1.0")

# Static & Templates with absolute paths
static_dir = BASE_DIR / "static"
templates_dir = BASE_DIR / "templates"

if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

templates = Jinja2Templates(directory=str(templates_dir))

brain = AIBrain()
owner = os.getenv("OWNER_NAME", "Sir")
commands = CommandHandler(owner_name=owner)

class ChatRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "jarvis_name": os.getenv("JARVIS_NAME", "JARVIS"),
        "owner_name": owner,
        "ready": brain.is_ready()
    })

@app.post("/api/chat")
async def chat(req: ChatRequest):
    if not brain.is_ready():
        return JSONResponse({
            "reply": "OpenAI API key is missing. Please set OPENAI_API_KEY in Vercel Environment Variables.",
            "error": True
        })

    text = req.message.strip()
    if not text:
        return JSONResponse({"reply": "I didn't catch that.", "error": False})

    response = commands.handle(text)

    if response == "GOODBYE":
        brain.reset_history()
        return JSONResponse({"reply": f"Goodbye {owner}. Session cleared.", "error": False})

    if response is None:
        response = brain.ask(text, owner_name=owner)

    return JSONResponse({"reply": response, "error": False})

@app.get("/api/status")
async def status():
    return {
        "status": "online",
        "ai_ready": brain.is_ready(),
        "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "name": os.getenv("JARVIS_NAME", "JARVIS")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("web_app:app", host="0.0.0.0", port=8000, reload=True)
