from agents.flight_agent import FlightAgent

agent = FlightAgent()

result = agent.search_flights(
    "Bangalore",
    "Goa"
)

print(result)