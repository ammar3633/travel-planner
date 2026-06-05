from agents.hotel_agent import HotelAgent
from agents.itinerary_agent import ItineraryAgent
from agents.expense_agent import ExpenseAgent
import asyncio
from adk_runner import get_flight, get_weather, get_attractions

class PlannerAgent:
    def __init__(self):
        self.hotel = HotelAgent()
        self.itinerary = ItineraryAgent()
        self.expense = ExpenseAgent()

    def create_plan(self, source, destination):
        flight = asyncio.run(get_flight(source, destination))
        weather = asyncio.run(get_weather(destination))
        attractions = asyncio.run(get_attractions(destination))
        hotel = self.hotel.search_hotels(destination)
        itinerary = self.itinerary.create_itinerary(
            source, destination, flight, hotel, weather
        )
        expenses = self.expense.calculate_expenses(
            source, destination, flight, hotel
        )
        return {
            "flight": flight,
            "hotel": hotel,
            "weather": weather,
            "attractions": attractions,
            "itinerary": itinerary,
            "expenses": expenses
        }