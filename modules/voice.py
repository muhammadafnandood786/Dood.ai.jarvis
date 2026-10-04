import speech_recognition as sr
import pyttsx3
import threading
import queue

class VoiceEngine:
    def __init__(self, rate: int = 175, volume: float = 1.0):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", rate)
        self.engine.setProperty("volume", volume)

        # Prefer a good English voice if available
        voices = self.engine.getProperty("voices")
        for voice in voices:
            if "english" in voice.name.lower() or "en_" in voice.id.lower() or "david" in voice.name.lower():
                self.engine.setProperty("voice", voice.id)
                break

        self.speaking = False
        self._speak_queue = queue.Queue()

    def speak(self, text: str, wait: bool = True):
        """Speak the given text."""
        print(f"JARVIS: {text}")
        if wait:
            self.engine.say(text)
            self.engine.runAndWait()
        else:
            def _speak():
                self.engine.say(text)
                self.engine.runAndWait()
            threading.Thread(target=_speak, daemon=True).start()

    def listen(self, timeout: int = 5, phrase_time_limit: int = 10) -> str | None:
        """Listen from microphone and return recognized text."""
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                print("Recognizing...")
                text = self.recognizer.recognize_google(audio)
                print(f"You: {text}")
                return text
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                print("Could not understand audio")
                return None
            except sr.RequestError as e:
                print(f"Speech recognition service error: {e}")
                return None
            except Exception as e:
                print(f"Listen error: {e}")
                return None

    def listen_continuous(self, wake_word: str = "jarvis"):
        """
        Generator that yields text when wake word is detected + command.
        Simple version: always listening for any speech.
        """
        while True:
            text = self.listen(timeout=None, phrase_time_limit=8)
            if text:
                yield text
