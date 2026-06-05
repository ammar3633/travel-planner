import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gemini_client import ask_gemini

class HotelAgent:
    def search_hotels(self, destination):
        prompt = f"Suggest a good hotel in {destination}. Include hotel name, price per night in INR, and rating. Be concise."
        return ask_gemini(prompt)