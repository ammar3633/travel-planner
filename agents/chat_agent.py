import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gemini_client import ask_gemini

class ChatAgent:
    def __init__(self):
        self.context = ""

    def set_context(self, source, destination, flight, hotel, weather, itinerary, expenses):
        self.context = f"""
        You are a helpful travel assistant. You have already planned a trip with these details:
        
        Trip: {source} to {destination}
        Flight: {flight}
        Hotel: {hotel}
        Weather: {weather}
        Itinerary: {itinerary}
        Expenses: {expenses}
        
        Answer any follow-up questions the user has about their trip.
        Be helpful, friendly and concise.
        """

    def chat(self, user_message):
        prompt = f"{self.context}\n\nUser question: {user_message}"
        return ask_gemini(prompt)