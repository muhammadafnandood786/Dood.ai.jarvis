import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class AIBrain:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None
        self.conversation_history = []
        self.system_prompt = """You are JARVIS, a highly advanced AI assistant inspired by Iron Man's JARVIS.
You are helpful, witty, efficient, slightly sarcastic in a British butler style, and always address the user as 'Sir' or the configured owner name.
Keep responses concise unless asked for detail.
You can control systems, answer questions, give suggestions, and help with daily tasks.
If the user asks to open something, search, or perform a system action, acknowledge and confirm.
Current year is 2026."""

    def is_ready(self) -> bool:
        return self.client is not None

    def ask(self, user_message: str, owner_name: str = "Sir") -> str:
        if not self.client:
            return "OpenAI API key missing. Please set OPENAI_API_KEY in .env file."

        # Update system prompt with owner name
        system = self.system_prompt.replace("Sir", owner_name)

        self.conversation_history.append({"role": "user", "content": user_message})

        # Keep history manageable
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system},
                    *self.conversation_history
                ],
                max_tokens=500,
                temperature=0.7,
            )
            reply = response.choices[0].message.content.strip()
            self.conversation_history.append({"role": "assistant", "content": reply})
            return reply
        except Exception as e:
            return f"Sorry {owner_name}, I encountered an error: {str(e)}"

    def reset_history(self):
        self.conversation_history = []
