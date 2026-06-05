import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gemini_client import ask_gemini

class ExpenseAgent:
    def calculate_expenses(self, source, destination, flight, hotel, days=3):
        prompt = f"""
        Calculate a complete travel expense breakdown for a {days}-day trip from {source} to {destination}.
        
        Known costs:
        - Flight: {flight}
        - Hotel: {hotel}
        
        Provide a detailed breakdown in this exact format:
        
        FLIGHT COST: ₹XXXX
        HOTEL COST (per night): ₹XXXX
        HOTEL TOTAL ({days} nights): ₹XXXX
        FOOD & DINING (per day): ₹XXXX
        FOOD TOTAL ({days} days): ₹XXXX
        LOCAL TRANSPORT (per day): ₹XXXX
        TRANSPORT TOTAL ({days} days): ₹XXXX
        ATTRACTIONS & ACTIVITIES: ₹XXXX
        MISCELLANEOUS: ₹XXXX
        GRAND TOTAL: ₹XXXX
        
        Be realistic with Indian Rupee estimates.
        """
        return ask_gemini(prompt)