<div align="center">

# ✈️ Voyager AI
### Multi-Agent Travel Planner

*Built with Google ADK · MCP · Gemini 2.5 Flash · Streamlit*

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Google ADK](https://img.shields.io/badge/Google_ADK-2.1-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-2.5_Flash-8B5CF6?style=for-the-badge&logo=google&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![MCP](https://img.shields.io/badge/MCP-FastMCP_3.4-10B981?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

> Type two cities → get real flights, live weather, hotel picks, local attractions, a 3-day itinerary, full expense breakdown, and an AI chat assistant — powered by 6 AI agents talking to each other in real time.

</div>

---

## 📸 Screenshots

### 🏠 Hero — Search Page
![Hero](screenshots/hero.png)

### ✈️ Results — Flights, Hotel & Weather
![Results](screenshots/results.png)

### 🗺️ Interactive Itinerary Builder
| Day 1 | Day 2 | Day 3 |
|-------|-------|-------|
| ![Day 1](screenshots/itinerary.png) | ![Day 2](screenshots/day2.png) | ![Day 3](screenshots/day3.png) |

### 💰 Expense Dashboard
![Expense](screenshots/expense.png)

### 💬 AI Travel Chat Assistant
![Chat](screenshots/chat.png)

---

## 🧠 How It Works

```
┌─────────────────────────────────────────────┐
│            Streamlit UI (app.py)            │
└───────────────────┬─────────────────────────┘
                    │ user inputs source + destination
                    ▼
┌─────────────────────────────────────────────┐
│         PlannerAgent  (A2A Orchestrator)    │
└──┬──────────┬──────────┬────────────────────┘
   │          │          │
   ▼          ▼          ▼
Flight     Weather    Hotel / Itinerary / Expense / Chat
Agent      Agent      Agents (Gemini powered)
   │          │
   ▼          ▼
┌─────────────────────────────────────────────┐
│           MCP Server  (port 8000)           │
│  search_flights · get_weather · attractions │
└──┬──────────┬──────────┬────────────────────┘
   │          │          │
   ▼          ▼          ▼
RapidAPI  QuickWeather  Wikipedia
Flights      API          API
```

---

## 🤖 Agent Breakdown

| Agent | Framework | Source |
|-------|-----------|--------|
| ✈️ Flight Search Agent | Google ADK `LlmAgent` | RapidAPI Flight Scanner — **real prices & times** |
| 🌤️ Weather Agent | Google ADK `LlmAgent` | QuickWeather API — **live temperature & conditions** |
| 🏨 Hotel Agent | Gemini 2.5 Flash | AI-curated recommendations |
| 🗺️ Itinerary Agent | Gemini 2.5 Flash | Day-by-day plan using real flight/weather context |
| 💰 Expense Agent | Gemini 2.5 Flash | Full INR cost breakdown |
| 💬 Chat Agent | Gemini 2.5 Flash | Context-aware travel Q&A |

---

## 🔌 MCP Server Tools

| Tool | API | What it returns |
|------|-----|-----------------|
| `search_flights` | RapidAPI Flight Scanner | Airline, price, departure time, duration |
| `get_weather` | QuickWeather | Temp, feels-like, condition, humidity, wind |
| `get_attractions` | Wikipedia | Top tourist spots with descriptions |

---

## 🛠️ Tech Stack

- **[Google ADK 2.1](https://google.github.io/adk-docs/)** — Agent Development Kit
- **[FastMCP 3.4](https://github.com/jlowin/fastmcp)** — MCP server framework
- **[Gemini 2.5 Flash](https://aistudio.google.com)** — Google's fastest LLM
- **[Streamlit](https://streamlit.io)** — Python web UI
- **[RapidAPI](https://rapidapi.com)** — Flight & weather APIs

---

## ⚡ Quick Start

### 1. Clone
```bash
git clone https://github.com/ammar3633/travel-planner.git
cd travel-planner
```

### 2. Virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install google-adk fastmcp uvicorn streamlit google-genai python-dotenv requests
```

### 4. Add API keys
Create a `.env` file:
```env
GEMINI_API_KEY=your_key_here
RAPIDAPI_KEY=your_key_here
```

| Key | Get it from |
|-----|------------|
| `GEMINI_API_KEY` | [aistudio.google.com](https://aistudio.google.com) — free |
| `RAPIDAPI_KEY` | [rapidapi.com](https://rapidapi.com) — subscribe to **Flight Scanner10** + **QuickWeather** |

### 5. Run

**Terminal 1 — MCP Server:**
```bash
python -c "import uvicorn, mcp_server; uvicorn.run(mcp_server.mcp.http_app(), host='0.0.0.0', port=8000)"
```

**Terminal 2 — App:**
```bash
streamlit run app.py
```

Open → `http://localhost:8501`

---

## 📁 Project Structure

```
travel-planner/
│
├── 📄 app.py                  # Streamlit UI (Airbnb-style)
├── 📄 mcp_server.py           # FastMCP server
├── 📄 adk_agents.py           # ADK LlmAgent definitions
├── 📄 adk_runner.py           # Async ADK runner
├── 📄 gemini_client.py        # Gemini API wrapper
│
├── 📁 agents/
│   ├── planner_agent.py       # A2A orchestrator
│   ├── flight_agent.py        # Real flights via MCP
│   ├── hotel_agent.py         # Hotel recommendations
│   ├── weather_agent.py       # Live weather via MCP
│   ├── itinerary_agent.py     # 3-day itinerary
│   ├── expense_agent.py       # Cost breakdown
│   └── chat_agent.py          # Travel assistant
│
├── 📁 screenshots/            # App screenshots
├── 📄 .env                    # API keys (not committed)
└── 📄 .gitignore
```

---

## ✅ Feature Checklist

- [x] Flight Search Agent — real API via MCP
- [x] Hotel Recommendation Agent
- [x] Weather Information Agent — live API via MCP
- [x] Itinerary Planning Agent
- [x] Travel API MCP Server
- [x] Weather MCP Server
- [x] Maps/Attractions MCP Server
- [x] A2A Communication — PlannerAgent orchestrates all
- [x] Travel Planning Portal — Airbnb-style UI
- [x] Interactive Itinerary Builder — editable Day 1/2/3
- [x] Expense Dashboard — full INR breakdown
- [x] Travel Chat Assistant — context-aware

---

## 👤 Author

**Mohammed Ammar**  
Built end-to-end in one day using Google ADK + MCP 🚀

---

<div align="center">
  <sub>Made with ❤️ · voyager.ai © 2026</sub>
</div>
