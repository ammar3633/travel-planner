import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gemini_client import ask_gemini

class ItineraryAgent:
    def create_itinerary(self, source, destination, flight, hotel, weather):
        prompt = f"""
        Create a detailed 3-day travel itinerary for a trip from {source} to {destination}.
        
        Context:
        - Flight: {flight}
        - Hotel: {hotel}
        - Weather: {weather}
        
        Return the itinerary in this EXACT format with these EXACT markers:
        
        ##DAY1##
        Morning: [morning activity and restaurant]
        Afternoon: [afternoon activity and restaurant]
        Evening: [evening activity and restaurant]
        ##DAY2##
        Morning: [morning activity and restaurant]
        Afternoon: [afternoon activity and restaurant]
        Evening: [evening activity and restaurant]
        ##DAY3##
        Morning: [morning activity and restaurant]
        Afternoon: [afternoon activity and restaurant]
        Evening: [evening activity and restaurant]
        
        Be specific, realistic and exciting. Include restaurant recommendations.
        """
        return ask_gemini(prompt)