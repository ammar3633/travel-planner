# ✈️ Voyager AI — Multi-Agent Travel Planner

A production-grade AI travel planner built with **Google ADK**, **MCP (Model Context Protocol)**, and **Gemini** — featuring real flight data, live weather, and a full itinerary generator.

---

## 🚀 Demo

> Type any two cities → Get real flights, live weather, hotel recommendations, local attractions, a 3-day itinerary, expense breakdown, and an AI chat assistant — all in one click.

---

## 🏗️ Architecture

```
User (Streamlit UI)
        ↓
  PlannerAgent (A2A Orchestrator)
        ↓
┌───────────┬───────────┬───────────┬───────────┬───────────┐
│  Flight   │   Hotel   │  Weather  │ Itinerary │  Expense  │
│  Agent    │   Agent   │   Agent   │   Agent   │   Agent   │
└─────┬─────┴───────────┴─────┬─────┴───────────┴───────────┘
      ↓                       ↓
 MCP Server (port 8000)
      ↓
┌─────────────┬──────────────┬─────────────┐
│ RapidAPI    │ QuickWeather │  Wikipedia  │
│ Flights     │     API      │ Attractions │
└─────────────┴──────────────┴─────────────┘
```

---

## 🤖 Agents

| Agent | Type | Data Source |
|-------|------|-------------|
| Flight Search Agent | ADK LlmAgent | RapidAPI Flight Scanner (real flights) |
| Hotel Agent | Gemini | AI-generated recommendations |
| Weather Agent | ADK LlmAgent | QuickWeather API (live data) |
| Itinerary Agent | Gemini | AI-generated day-by-day plan |
| Expense Agent | Gemini | AI-generated cost breakdown |
| Chat Agent | Gemini | Context-aware travel assistant |

---

## 🔌 MCP Servers

| Tool | API | Data |
|------|-----|------|
| `search_flights` | RapidAPI Flight Scanner | Real-time flight prices & schedules |
| `get_weather` | QuickWeather API | Live temperature, condition, humidity |
| `get_attractions` | Wikipedia API | Local tourist attractions |

---

## 🛠️ Tech Stack

- **Google ADK 2.1** — Agent Development Kit
- **FastMCP 3.4** — MCP server framework
- **Gemini 2.5 Flash** — LLM for all agents
- **Streamlit** — Frontend UI
- **RapidAPI** — Flight & weather data
- **Python 3.13**

---

## 📦 Installation

### 1. Clone the repo
```bash
git clone https://github.com/ammar3633/travel-planner.git
cd travel-planner
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Install dependencies
```bash
pip install google-adk fastmcp uvicorn streamlit google-genai python-dotenv requests
```

### 4. Set up API keys
Create a `.env` file in the root folder:
```
GEMINI_API_KEY=your_gemini_api_key
RAPIDAPI_KEY=your_rapidapi_key
```

Get your keys from:
- Gemini → [aistudio.google.com](https://aistudio.google.com)
- RapidAPI → [rapidapi.com](https://rapidapi.com) (subscribe to **Flight Scanner10** and **QuickWeather**)

---

## ▶️ Running the App

You need **two terminals** open:

**Terminal 1 — Start MCP Server:**
```bash
python -c "import uvicorn, mcp_server; uvicorn.run(mcp_server.mcp.http_app(), host='0.0.0.0', port=8000)"
```

**Terminal 2 — Start Streamlit App:**
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 📁 Project Structure

```
travel-planner/
├── app.py                  # Streamlit UI
├── mcp_server.py           # FastMCP server (flights, weather, attractions)
├── adk_agents.py           # ADK LlmAgent definitions
├── adk_runner.py           # ADK async runner
├── gemini_client.py        # Gemini API client
├── agents/
│   ├── flight_agent.py     # Flight search (via MCP)
│   ├── hotel_agent.py      # Hotel recommendations
│   ├── weather_agent.py    # Weather (via MCP)
│   ├── itinerary_agent.py  # Day-by-day itinerary
│   ├── expense_agent.py    # Cost breakdown
│   ├── chat_agent.py       # Travel chat assistant
│   └── planner_agent.py    # A2A orchestrator
└── .env                    # API keys (not committed)
```

---

## ✅ Use Case Checklist

| Requirement | Status |
|-------------|--------|
| Flight Search Agent | ✅ Real API via MCP |
| Hotel Recommendation Agent | ✅ Gemini powered |
| Weather Information Agent | ✅ Live API via MCP |
| Itinerary Planning Agent | ✅ Gemini powered |
| Travel API MCP | ✅ RapidAPI Flight Scanner |
| Weather MCP | ✅ QuickWeather API |
| Maps MCP | ✅ Wikipedia Attractions |
| A2A Communication | ✅ PlannerAgent orchestrates all |
| Travel Planning Portal | ✅ Airbnb-style Streamlit UI |
| Interactive Itinerary Builder | ✅ Editable Day 1/2/3 tabs |
| Expense Dashboard | ✅ Full INR breakdown |
| Travel Chat Assistant | ✅ Context-aware chat |

---

## 👤 Author

**Mohammed Ammar**  
Built with Google ADK + MCP in one day 🚀

---

## 📄 License

MIT License
