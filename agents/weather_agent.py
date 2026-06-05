import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gemini_client import ask_gemini

class WeatherAgent:
    def get_weather(self, destination):
        prompt = f"Give current weather summary for {destination}. Include temperature and condition. Be concise."
        return ask_gemini(prompt)