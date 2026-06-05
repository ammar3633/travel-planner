import sys
import os
import requests
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
from gemini_client import ask_gemini
load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
HOST = "flight-scanner10.p.rapidapi.com"

class FlightAgent:
    def get_airport_id(self, city):
        url = f"https://{HOST}/api/v3/flights/searchAirport"
        headers = {
            "x-rapidapi-host": HOST,
            "x-rapidapi-key": RAPIDAPI_KEY
        }
        params = {"query": city, "locale": "en-GB"}
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        places = data.get("data", [])
        if places:
            return places[0]["navigation"]["entityId"]
        return None

    def search_flights(self, source, destination):
        origin_id = self.get_airport_id(source)
        dest_id = self.get_airport_id(destination)

        if not origin_id or not dest_id:
            return f"Could not find airports for {source} or {destination}"

        from datetime import datetime, timedelta
        depart_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")

        url = f"https://{HOST}/api/v3/flights/searchFlights"
        headers = {
            "x-rapidapi-host": HOST,
            "x-rapidapi-key": RAPIDAPI_KEY,
            "Content-Type": "application/json"
        }
        body = {
            "originEntityId": origin_id,
            "destinationEntityId": dest_id,
            "departureDate": depart_date,
            "adults": 1,
            "cabinClass": "economy",
            "currencyCode": "INR",
            "locale": "en-GB",
            "market": "IN"
        }

        # First call
        response = requests.post(url, headers=headers, json=body)
        data = response.json()

        # Poll if incomplete
        session_id = data.get("data", {}).get("context", {}).get("sessionId")
        status = data.get("data", {}).get("context", {}).get("status")
        itineraries = data.get("data", {}).get("itineraries")

        attempts = 0
        while status == "incomplete" and not itineraries and attempts < 5:
            time.sleep(2)
            body["sessionId"] = session_id
            response = requests.post(url, headers=headers, json=body)
            data = response.json()
            status = data.get("data", {}).get("context", {}).get("status")
            itineraries = data.get("data", {}).get("itineraries")
            attempts += 1

        if not itineraries:
            # Fallback to Gemini
            return ask_gemini(f"Suggest a realistic flight from {source} to {destination}. Include airline, price in INR, departure time, duration. Be concise.")

        # Parse top 3
        results = []
        for flight in itineraries[:3]:
            price = flight.get("price", {}).get("formatted", "N/A")
            legs = flight.get("legs", [])
            if legs:
                leg = legs[0]
                airline = leg.get("carriers", {}).get("marketing", [{}])[0].get("name", "Unknown")
                departure = leg.get("departure", "")[:16]
                duration = leg.get("durationInMinutes", 0)
                hours = duration // 60
                mins = duration % 60
                results.append(f"✈ {airline} — {price} — Departs: {departure} — Duration: {hours}h {mins}m")

        return "\n".join(results) if results else ask_gemini(f"Suggest a realistic flight from {source} to {destination}. Include airline, price in INR, departure time, duration. Be concise.")