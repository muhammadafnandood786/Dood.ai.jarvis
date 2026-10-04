# JARVIS AI Assistant (Pure Python + OpenAI)

A practical **JARVIS-like** voice & text AI assistant inspired by Iron Man.

**Repo:** https://github.com/muhammadafnandood786/Dood.ai.jarvis

**Works on:**
- PC / Laptop (full local voice mode)
- Mobile / Tablet / Any browser (Web UI with voice)
- 24/7 ready (run as service or deploy)

---

## Features

- Voice input & output (local + browser)
- OpenAI GPT brain (smart, context-aware replies)
- Local commands: time, date, open websites, Google/YouTube search, system status, Wikipedia, weather
- Beautiful dark cyber UI
- Modular & easy to extend
- Deployable on **Vercel**

---

## Quick Start (Local PC / Laptop)

### 1. Clone & Setup

```bash
git clone https://github.com/muhammadafnandood786/Dood.ai.jarvis.git
cd Dood.ai.jarvis

python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Add OpenAI Key

```bash
cp .env.example .env
```

Edit `.env` and put your key:

```
OPENAI_API_KEY=sk-your-real-key-here
OPENAI_MODEL=gpt-4o-mini
OWNER_NAME=Sir
JARVIS_NAME=JARVIS
```

Get key from: https://platform.openai.com/api-keys

### 3. Run Local Voice Mode (Best for PC)

```bash
python local_jarvis.py
```

Speak naturally. Say **"goodbye"** or **"exit"** to quit.

### 4. Run Web Mode (Mobile + PC Browser)

```bash
python web_app.py
```

Open: http://localhost:8000

Works great on phone browser too (use Chrome for best voice support).

---

## Deploy on Vercel (24/7 Web Access)

1. Go to [vercel.com](https://vercel.com) → New Project → Import this repo
2. Add Environment Variable:
   - `OPENAI_API_KEY` = your key
   - (optional) `OPENAI_MODEL`, `OWNER_NAME`
3. Deploy

Your JARVIS will be live at `https://your-project.vercel.app`

**Note:** Vercel is serverless → perfect for web chat/voice. Continuous always-listening needs local run or a VPS.

---

## Local Commands (work without OpenAI too)

| Say / Type                  | Action                          |
|----------------------------|---------------------------------|
| What time is it?           | Current time                    |
| What's the date?           | Today's date                    |
| Open YouTube / Google / GitHub / Gmail / WhatsApp / Netflix etc. | Opens website |
| Search for quantum computing | Google search                 |
| Play shape of you on YouTube | YouTube search               |
| System status / CPU / Battery | System info                  |
| Who is Elon Musk / Wikipedia ... | Wikipedia summary         |
| Weather in Lahore          | Weather (needs free API key)    |
| Goodbye / Exit             | Quit                            |

Everything else goes to OpenAI brain.

---

## Optional: Weather

1. Free key: https://openweathermap.org/api
2. Add to `.env`: `WEATHER_API_KEY=your_key`

---

## Android (Termux) Quick Tip

```bash
pkg install python
pip install -r requirements.txt
# Then run web_app.py and open in browser
# Local mic voice is limited on Termux
```

---

## Project Structure

```
Dood.ai.jarvis/
├── local_jarvis.py      # Full voice mode for desktop
├── web_app.py           # FastAPI web server (mobile + PC)
├── modules/
│   ├── ai_brain.py      # OpenAI integration
│   ├── commands.py      # Local command handlers
│   └── voice.py         # Speech recognition + TTS
├── templates/index.html # Beautiful UI
├── requirements.txt
├── .env.example
└── vercel.json
```

---

## Extend It

Add new commands in `modules/commands.py` → `handle()` method.

Change personality in `modules/ai_brain.py` → `system_prompt`.

---

## Important Notes

- **True movie JARVIS** (full computer control + continuous listening + suit integration) needs OS-level permissions and is only possible when running **locally**.
- Web version is safe and works everywhere.
- Never share your `.env` or API key.
- Microphone permission required for voice.

---

**Made for 2026 • Pure Python • OpenAI Powered**

Say the word and JARVIS will assist you.
