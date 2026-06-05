import os
import requests
from dotenv import load_dotenv
from fastmcp import FastMCP
import uvicorn

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
HOST = "flight-scanner10.p.rapidapi.com"

mcp = FastMCP("Travel MCP Server")

@mcp.tool()
def search_airport(city: str) -> str:
    """Search for airport entity ID by city name"""
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
        entity_id = places[0]["navigation"]["entityId"]
        name = places[0]["presentation"]["title"]
        return f"{name}:{entity_id}"
    return "NOT_FOUND"

@mcp.tool()
def search_flights(origin_city: str, destination_city: str, depart_date: str) -> str:
    """Search real flights between two cities on a given date (YYYY-MM-DD)"""
    import time

    origin_data = search_airport(origin_city)
    dest_data = search_airport(destination_city)

    if "NOT_FOUND" in origin_data or "NOT_FOUND" in dest_data:
        return f"Airport not found for {origin_city} or {destination_city}"

    origin_id = origin_data.split(":")[1]
    dest_id = dest_data.split(":")[1]

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

    response = requests.post(url, headers=headers, json=body)
    data = response.json()

    itineraries = data.get("data", {}).get("itineraries")
    session_id = data.get("data", {}).get("context", {}).get("sessionId")
    status = data.get("data", {}).get("context", {}).get("status")

    attempts = 0
    while (not itineraries or len(itineraries) == 0) and attempts < 5:
        time.sleep(2)
        body["sessionId"] = session_id
        response = requests.post(url, headers=headers, json=body)
        data = response.json()
        itineraries = data.get("data", {}).get("itineraries")
        status = data.get("data", {}).get("context", {}).get("status")
        attempts += 1
        if status == "complete":
            break

    if not itineraries:
        return "No flights found"

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
            results.append(f"{airline} | {price} | Departs: {departure} | Duration: {hours}h {mins}m")

    return "\n".join(results) if results else "No flights found"

@mcp.tool()
def get_weather(city: str) -> str:
    """Get current weather for a city"""
    url = "https://quickweather.p.rapidapi.com/current"
    headers = {
        "x-rapidapi-host": "quickweather.p.rapidapi.com",
        "x-rapidapi-key": RAPIDAPI_KEY
    }
    params = {"city": city}
    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        current = data.get("current", {})
        temp = current.get("temperature", "N/A")
        feels_like = current.get("feels_like", "N/A")
        condition = current.get("weather", "N/A")
        humidity = current.get("humidity", "N/A")
        wind = current.get("wind_speed", "N/A")
        return f"Temperature: {temp}°C | Feels like: {feels_like}°C | Condition: {condition} | Humidity: {humidity}% | Wind: {wind} km/h"
    except Exception as e:
        return f"Weather data unavailable for {city}: {str(e)}"

@mcp.tool()
def get_attractions(city: str) -> str:
    """Get top tourist attractions for a city using Wikipedia"""
    try:
        url = "https://en.wikipedia.org/w/api.php"
        headers = {"User-Agent": "TravelPlannerApp/1.0 (contact@example.com)"}
        params = {
            "action": "query",
            "list": "search",
            "srsearch": f"tourist attractions {city}",
            "format": "json",
            "srlimit": 5
        }
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        results = data.get("query", {}).get("search", [])

        if not results:
            return f"No attractions found for {city}"

        attractions = []
        for r in results[:5]:
            title = r.get("title", "N/A")
            snippet = r.get("snippet", "").replace("<span class=\"searchmatch\">", "").replace("</span>", "")
            attractions.append(f"📍 {title} — {snippet[:80]}...")

        return "\n".join(attractions)

    except Exception as e:
        return f"Attractions unavailable for {city}: {str(e)}"