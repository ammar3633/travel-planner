import asyncio
import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset, StreamableHTTPConnectionParams
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

load_dotenv()

async def run_agent(agent, message):
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=agent.name,
        user_id="user1",
        session_id="session1"
    )
    runner = Runner(
        agent=agent,
        app_name=agent.name,
        session_service=session_service
    )
    content = Content(role="user", parts=[Part(text=message)])
    response_text = ""
    async for event in runner.run_async(
        user_id="user1",
        session_id="session1",
        new_message=content
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                response_text = event.content.parts[0].text
    return response_text

async def get_flight(source, destination):
    from adk_agents import create_flight_agent
    agent = create_flight_agent()
    return await run_agent(agent, f"Find flights from {source} to {destination}")

async def get_weather(city):
    from adk_agents import create_weather_agent
    agent = create_weather_agent()
    return await run_agent(agent, f"Get weather for {city}")

async def get_attractions(city):
    from adk_agents import create_attractions_agent
    agent = create_attractions_agent()
    return await run_agent(agent, f"Get top tourist attractions in {city}")

if __name__ == "__main__":
    async def test():
        print("Testing Flight Agent...")
        flight = await get_flight("Bangalore", "Dubai")
        print("FLIGHT:", flight)
        print("\nTesting Weather Agent...")
        weather = await get_weather("Dubai")
        print("WEATHER:", weather)
        print("\nTesting Attractions Agent...")
        attractions = await get_attractions("Dubai")
        print("ATTRACTIONS:", attractions)

    asyncio.run(test())