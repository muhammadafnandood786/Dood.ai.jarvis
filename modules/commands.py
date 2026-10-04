import os
import webbrowser
import datetime
import platform
import psutil
import wikipedia
import requests
from dotenv import load_dotenv

load_dotenv()

class CommandHandler:
    def __init__(self, owner_name: str = "Sir"):
        self.owner_name = owner_name
        self.weather_key = os.getenv("WEATHER_API_KEY")

    def handle(self, text: str) -> str | None:
        """
        Try to handle common commands.
        Returns response string if handled, else None (fall back to AI).
        """
        text_lower = text.lower().strip()

        # Time
        if any(w in text_lower for w in ["time", "what time", "current time"]):
            now = datetime.datetime.now().strftime("%I:%M %p")
            return f"The current time is {now}, {self.owner_name}."

        # Date
        if any(w in text_lower for w in ["date", "what day", "today's date", "day today"]):
            today = datetime.datetime.now().strftime("%A, %d %B %Y")
            return f"Today is {today}, {self.owner_name}."

        # Open websites
        sites = {
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
            "github": "https://github.com",
            "gmail": "https://mail.google.com",
            "whatsapp": "https://web.whatsapp.com",
            "twitter": "https://x.com",
            "x": "https://x.com",
            "facebook": "https://www.facebook.com",
            "instagram": "https://www.instagram.com",
            "linkedin": "https://www.linkedin.com",
            "netflix": "https://www.netflix.com",
            "spotify": "https://open.spotify.com",
            "chatgpt": "https://chat.openai.com",
            "wikipedia": "https://www.wikipedia.org",
        }
        for name, url in sites.items():
            if f"open {name}" in text_lower or f"open {name}.com" in text_lower:
                webbrowser.open(url)
                return f"Opening {name.capitalize()} for you, {self.owner_name}."

        # Search Google
        if text_lower.startswith("search ") or "search for" in text_lower or "google " in text_lower:
            query = text_lower.replace("search for", "").replace("search", "").replace("google", "").strip()
            if query:
                webbrowser.open(f"https://www.google.com/search?q={query}")
                return f"Searching Google for '{query}', {self.owner_name}."

        # YouTube search
        if "play" in text_lower and ("youtube" in text_lower or "song" in text_lower or "video" in text_lower):
            query = text_lower.replace("play", "").replace("on youtube", "").replace("youtube", "").replace("song", "").replace("video", "").strip()
            if query:
                webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
                return f"Searching YouTube for '{query}', {self.owner_name}."

        # System info
        if any(w in text_lower for w in ["system info", "system status", "cpu", "memory", "ram", "battery"]):
            return self._system_info()

        # Wikipedia
        if "wikipedia" in text_lower or text_lower.startswith("who is ") or text_lower.startswith("what is "):
            try:
                query = text_lower.replace("wikipedia", "").replace("who is", "").replace("what is", "").strip()
                if query:
                    summary = wikipedia.summary(query, sentences=2)
                    return f"According to Wikipedia: {summary}"
            except Exception:
                return f"Sorry {self.owner_name}, I couldn't find information on that."

        # Weather
        if "weather" in text_lower:
            city = "London"
            for word in text_lower.split():
                if word not in ["weather", "in", "the", "what", "is", "how's", "how", "today"]:
                    city = word
                    break
            return self._get_weather(city)

        # Exit / Sleep
        if any(w in text_lower for w in ["goodbye", "bye", "exit", "quit", "sleep", "shutdown jarvis"]):
            return "GOODBYE"

        return None

    def _system_info(self) -> str:
        cpu = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory()
        battery = psutil.sensors_battery()
        info = (
            f"System Status, {self.owner_name}:\n"
            f"• OS: {platform.system()} {platform.release()}\n"
            f"• CPU Usage: {cpu}%\n"
            f"• Memory: {mem.percent}% used ({mem.used // (1024**3)} GB / {mem.total // (1024**3)} GB)"
        )
        if battery:
            info += f"\n• Battery: {battery.percent}% {'(Charging)' if battery.power_plugged else '(Discharging)'}"
        return info

    def _get_weather(self, city: str) -> str:
        if not self.weather_key:
            return f"Weather API key not set, {self.owner_name}. Get a free key from openweathermap.org and add WEATHER_API_KEY to .env"
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_key}&units=metric"
            data = requests.get(url, timeout=5).json()
            if data.get("cod") != 200:
                return f"Couldn't find weather for {city}, {self.owner_name}."
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            feels = data["main"]["feels_like"]
            return f"Weather in {city.title()}: {temp}°C, {desc}. Feels like {feels}°C."
        except Exception as e:
            return f"Weather service unavailable right now, {self.owner_name}."
