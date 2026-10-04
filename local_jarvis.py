#!/usr/bin/env python3
"""
JARVIS - Local Voice Mode
Run this on your PC / Laptop for full voice interaction + system control.
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

from modules.ai_brain import AIBrain
from modules.commands import CommandHandler
from modules.voice import VoiceEngine

def main():
    owner = os.getenv("OWNER_NAME", "Sir")
    name = os.getenv("JARVIS_NAME", "JARVIS")

    print("=" * 50)
    print(f"  {name} - Local Voice Assistant")
    print("  OpenAI Powered | Pure Python")
    print("=" * 50)

    brain = AIBrain()
    if not brain.is_ready():
        print("\n[ERROR] OPENAI_API_KEY not found in .env")
        print("1. Copy .env.example to .env")
        print("2. Add your OpenAI API key")
        print("3. Run again\n")
        sys.exit(1)

    commands = CommandHandler(owner_name=owner)
    voice = VoiceEngine(rate=170)

    voice.speak(f"Hello {owner}. {name} online and ready.")

    print("\nSay something... (or 'goodbye' / 'exit' to quit)\n")

    while True:
        try:
            text = voice.listen(timeout=8, phrase_time_limit=12)
            if not text:
                continue

            # First try local commands
            response = commands.handle(text)

            if response == "GOODBYE":
                voice.speak(f"Goodbye {owner}. Shutting down.")
                break

            if response is None:
                # Fall back to AI brain
                response = brain.ask(text, owner_name=owner)

            voice.speak(response)

        except KeyboardInterrupt:
            print("\nInterrupted by user.")
            voice.speak(f"Going offline, {owner}.")
            break
        except Exception as e:
            print(f"Error: {e}")
            voice.speak("I encountered a small error. Please try again.")

if __name__ == "__main__":
    main()
