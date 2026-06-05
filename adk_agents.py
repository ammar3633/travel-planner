import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset, StreamableHTTPConnectionParams

load_dotenv()

def create_flight_agent():
    return LlmAgent(
        name="flight_agent",
        model="gemini-2.5-flash",
        description="Searches for real flights between cities using MCP tools",
        instruction="""You are a flight search agent.
        Use the search_flights tool to find real flights.
        Today is 2026-06-05, so use 2026-07-05 as the departure date.
        Call search_flights with origin_city, destination_city, and depart_date=2026-07-05.
        Return the results clearly.""",
        tools=[McpToolset(
            connection_params=StreamableHTTPConnectionParams(url="http://localhost:8000/mcp"),
            tool_filter=["search_flights", "search_airport"]
        )]
    )

def create_weather_agent():
    return LlmAgent(
        name="weather_agent",
        model="gemini-2.5-flash",
        description="Gets real weather data for cities using MCP tools",
        instruction="""You are a weather agent.
        Use the get_weather tool to fetch real weather data.
        Return temperature, condition and any travel advice.""",
        tools=[McpToolset(
            connection_params=StreamableHTTPConnectionParams(url="http://localhost:8000/mcp"),
            tool_filter=["get_weather"]
        )]
    )

def create_attractions_agent():
    return LlmAgent(
        name="attractions_agent",
        model="gemini-2.5-flash",
        description="Gets real tourist attractions for cities using Google Maps MCP",
        instruction="""You are a local attractions agent.
        Use the get_attractions tool to find top tourist spots.
        Return the top attractions with ratings clearly.""",
        tools=[McpToolset(
            connection_params=StreamableHTTPConnectionParams(url="http://localhost:8000/mcp"),
            tool_filter=["get_attractions"]
        )]
    )