import streamlit as st
from agents.planner_agent import PlannerAgent
from agents.chat_agent import ChatAgent
import requests
import os
from dotenv import load_dotenv

load_dotenv()
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

st.set_page_config(
    page_title="Voyager — AI Travel Planner",
    page_icon="🌍",
    layout="wide"
)

# Inject CSS via components
import streamlit.components.v1 as components

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; }

body, .stApp {
  background: #f7f7f7 !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
}

.stApp > header { background: transparent !important; }
[data-testid="stAppViewContainer"] > .main { padding: 0 !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
#MainMenu, footer, .stDeployButton { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }

.stTextInput > div > div > input {
  background: #fff !important;
  border: 1.5px solid #ebebeb !important;
  border-radius: 12px !important;
  color: #222 !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-size: 15px !important;
  font-weight: 500 !important;
  padding: 14px 16px !important;
}
.stTextInput > div > div > input:focus {
  border-color: #FF385C !important;
  box-shadow: 0 0 0 3px rgba(255,56,92,0.12) !important;
  background: #fff !important;
}
.stTextInput label {
  color: #222 !important;
  font-size: 11px !important;
  font-weight: 700 !important;
  letter-spacing: 1.5px !important;
  text-transform: uppercase !important;
}
.stTextInput > div { border: none !important; }

.stButton > button {
  background: linear-gradient(135deg, #FF385C, #E61E4D) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 12px !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-size: 15px !important;
  font-weight: 700 !important;
  padding: 14px 28px !important;
  width: 100% !important;
  height: auto !important;
  transition: all 0.2s ease !important;
  box-shadow: 0 4px 15px rgba(255,56,92,0.3) !important;
}
.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 25px rgba(255,56,92,0.45) !important;
}

.stTabs [data-baseweb="tab-list"] {
  background: #f0f0f0 !important;
  border-radius: 10px !important;
  padding: 4px !important;
  border: none !important;
}
.stTabs [data-baseweb="tab"] {
  color: #717171 !important;
  border-radius: 8px !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-size: 13px !important;
  font-weight: 600 !important;
}
.stTabs [aria-selected="true"] {
  background: #fff !important;
  color: #FF385C !important;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none !important; }

.stTextArea textarea {
  background: #f7f7f7 !important;
  border: 1.5px solid #ebebeb !important;
  border-radius: 10px !important;
  color: #222 !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-size: 13px !important;
  line-height: 1.7 !important;
}
.stTextArea textarea:focus {
  border-color: #FF385C !important;
  box-shadow: 0 0 0 3px rgba(255,56,92,0.1) !important;
}

.stChatMessage { background: transparent !important; }
.stChatInputContainer > div {
  background: #fff !important;
  border: 1.5px solid #ebebeb !important;
  border-radius: 14px !important;
}
.stSpinner > div { border-top-color: #FF385C !important; }
hr { border-color: #ebebeb !important; margin: 24px 0 !important; }
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

# ── NAV ──
st.markdown("""
<div style="
  background:#fff;
  border-bottom:1px solid #ebebeb;
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:0 48px;
  height:72px;
  position:sticky;
  top:0;
  z-index:999;
">
  <div style="font-size:21px;font-weight:800;color:#FF385C;letter-spacing:-0.5px;font-family:'Plus Jakarta Sans',sans-serif">
    voyager<span style="color:#222">.ai</span>
  </div>
  <div style="display:flex;gap:28px;font-size:14px;font-weight:500;color:#717171;font-family:'Plus Jakarta Sans',sans-serif">
    <span>Explore</span><span>How it works</span><span>About</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── HERO ──
st.markdown("""
<div style="
  background:linear-gradient(135deg,#FF385C 0%,#E61E4D 40%,#BD1E59 70%,#8B2CF5 100%);
  padding:80px 48px 110px;
  text-align:center;
">
  <div style="
    display:inline-block;
    background:rgba(255,255,255,0.18);
    border:1px solid rgba(255,255,255,0.4);
    color:#fff;
    font-size:11px;
    font-weight:700;
    letter-spacing:2.5px;
    text-transform:uppercase;
    padding:7px 20px;
    border-radius:20px;
    margin-bottom:22px;
    font-family:'Plus Jakarta Sans',sans-serif;
  ">✦ Powered by 6 AI Agents + MCP</div>
  <h1 style="
    font-size:clamp(2.6rem,6vw,4.8rem);
    font-weight:800;
    color:#fff;
    line-height:1.1;
    letter-spacing:-2px;
    margin-bottom:14px;
    font-family:'Plus Jakarta Sans',sans-serif;
  ">Where do you want<br>to go next?</h1>
  <p style="
    font-size:17px;
    color:rgba(255,255,255,0.82);
    font-weight:400;
    font-family:'Plus Jakarta Sans',sans-serif;
  ">Real flights · Live weather · Hotels · Attractions · Full itinerary</p>
</div>
""", unsafe_allow_html=True)

# ── SEARCH ──
st.markdown("""
<div style="background:#f7f7f7;padding:0 48px;">
  <div style="
    max-width:900px;
    margin:-36px auto 0;
    background:#fff;
    border-radius:20px;
    box-shadow:0 12px 48px rgba(0,0,0,0.14);
    padding:20px 24px 16px;
    position:relative;
    z-index:10;
  ">
""", unsafe_allow_html=True)

sc1, sc2, sc3 = st.columns([5, 5, 3])
with sc1:
    source_input = st.text_input("🛫  FROM", placeholder="e.g. Mumbai, Bangalore…", key="source_input")
with sc2:
    dest_input = st.text_input("🛬  TO", placeholder="e.g. Dubai, Tokyo…", key="dest_input")
with sc3:
    st.markdown("<div style='height:29px'></div>", unsafe_allow_html=True)
    plan_btn = st.button("🔍  Search Trips", key="plan_btn")

st.markdown("</div></div>", unsafe_allow_html=True)

# ── AUTOCOMPLETE ──
def get_city_suggestions(query):
    if not query or len(query) < 2:
        return []
    try:
        url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities"
        headers = {
            "x-rapidapi-host": "wft-geo-db.p.rapidapi.com",
            "x-rapidapi-key": RAPIDAPI_KEY
        }
        params = {"namePrefix": query, "limit": 5, "languageCode": "en", "minPopulation": 100000}
        r = requests.get(url, headers=headers, params=params, timeout=3)
        data = r.json()
        return [{"city": i.get("city", i.get("name","")), "country": i.get("country","")} for i in data.get("data", [])]
    except:
        return []

st.markdown("<div style='padding:0 48px;max-width:900px;margin:0 auto;'>", unsafe_allow_html=True)

if source_input and len(source_input) >= 2:
    sugs = get_city_suggestions(source_input)
    if sugs:
        st.markdown("<p style='font-size:12px;font-weight:700;letter-spacing:1px;color:#717171;text-transform:uppercase;margin:12px 0 6px;font-family:Plus Jakarta Sans,sans-serif'>From — select city</p>", unsafe_allow_html=True)
        cols = st.columns(min(len(sugs), 5))
        for i, s in enumerate(sugs[:5]):
            with cols[i]:
                if st.button(f"📍 {s['city']}, {s['country']}", key=f"src_{i}"):
                    st.session_state.chosen_source = s['city']
                    st.rerun()

if dest_input and len(dest_input) >= 2:
    sugs2 = get_city_suggestions(dest_input)
    if sugs2:
        st.markdown("<p style='font-size:12px;font-weight:700;letter-spacing:1px;color:#717171;text-transform:uppercase;margin:12px 0 6px;font-family:Plus Jakarta Sans,sans-serif'>To — select city</p>", unsafe_allow_html=True)
        cols2 = st.columns(min(len(sugs2), 5))
        for i, s in enumerate(sugs2[:5]):
            with cols2[i]:
                if st.button(f"📍 {s['city']}, {s['country']}", key=f"dst_{i}"):
                    st.session_state.chosen_dest = s['city']
                    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

source = st.session_state.get("chosen_source", source_input)
destination = st.session_state.get("chosen_dest", dest_input)

# ── GENERATE ──
if plan_btn:
    if source and destination:
        with st.spinner("✈️ Your AI agents are crafting the perfect trip…"):
            planner = PlannerAgent()
            result = planner.create_plan(source, destination)
            st.session_state.result = result
            st.session_state.source = source
            st.session_state.destination = destination
            st.session_state.chat_agent = ChatAgent()
            st.session_state.chat_agent.set_context(
                source, destination,
                result["flight"], result["hotel"],
                result["weather"], result["itinerary"],
                result["expenses"]
            )
            st.session_state.messages = []
            st.session_state.itinerary_days = None
            st.session_state.itinerary_saved = False
            st.session_state.chosen_source = None
            st.session_state.chosen_dest = None
    else:
        st.warning("Please enter both cities to generate your travel plan.")

# ── RESULTS ──
if "result" in st.session_state:
    result = st.session_state.result
    src = st.session_state.source
    dest = st.session_state.destination

    st.markdown("<div style='padding:40px 48px;max-width:1280px;margin:0 auto;'>", unsafe_allow_html=True)

    # Route header
    st.markdown(f"""
    <div style="
      display:flex;align-items:center;justify-content:space-between;
      margin-bottom:32px;padding-bottom:24px;border-bottom:1px solid #ebebeb;
    ">
      <div>
        <div style="font-size:26px;font-weight:800;color:#222;letter-spacing:-0.5px;font-family:'Plus Jakarta Sans',sans-serif">
          {src.title()} → {dest.title()}
        </div>
        <div style="font-size:14px;color:#717171;margin-top:4px;font-family:'Plus Jakarta Sans',sans-serif">
          Your complete AI-generated travel plan · 3 days · Economy
        </div>
      </div>
      <div style="
        background:linear-gradient(135deg,#FF385C,#E61E4D);
        color:#fff;font-size:13px;font-weight:600;
        padding:10px 20px;border-radius:20px;
        font-family:'Plus Jakarta Sans',sans-serif;
      ">✦ 6 Agents · 3 MCP Servers</div>
    </div>
    """, unsafe_allow_html=True)

    def card_start(icon, label, title, color):
        st.markdown(f"""
        <div style="
          background:#fff;border:1px solid #ebebeb;border-radius:16px;
          overflow:hidden;margin-bottom:8px;
        ">
          <div style="
            padding:14px 20px 12px;border-bottom:1px solid #f7f7f7;
            display:flex;align-items:center;gap:10px;
          ">
            <div style="
              width:38px;height:38px;border-radius:10px;
              background:{color};display:flex;align-items:center;
              justify-content:center;font-size:18px;flex-shrink:0;
            ">{icon}</div>
            <div>
              <div style="font-size:10px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#aaa;font-family:'Plus Jakarta Sans',sans-serif">{label}</div>
              <div style="font-size:15px;font-weight:700;color:#222;font-family:'Plus Jakarta Sans',sans-serif">{title}</div>
            </div>
          </div>
          <div style="padding:16px 20px;">
        """, unsafe_allow_html=True)

    def card_end():
        st.markdown("</div></div>", unsafe_allow_html=True)

    # Row 1
    c1, c2, c3 = st.columns(3)
    with c1:
        card_start("✈️", "Real Flight Data", "Available Flights", "#FFF0F3")
        st.write(result["flight"])
        card_end()
    with c2:
        card_start("🏨", "AI Recommendation", "Where to Stay", "#F0FBF7")
        st.write(result["hotel"])
        card_end()
    with c3:
        card_start("🌤️", "Live Weather Data", "Current Weather", "#FFF8F0")
        st.write(result["weather"])
        card_end()

    # Attractions
    card_start("📍", "Via MCP · Wikipedia", "Local Attractions", "#F0FAF5")
    st.write(result["attractions"])
    card_end()

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # Row 2
    c4, c5 = st.columns([3, 2])

    with c4:
        card_start("✏️", "Editable · Day by Day", "Interactive Itinerary Builder", "#FAF0FF")

        if not st.session_state.get("itinerary_days"):
            itin = result["itinerary"]
            days = {"Day 1": "", "Day 2": "", "Day 3": ""}
            if "##DAY1##" in itin:
                parts = itin.split("##DAY")
                for part in parts[1:]:
                    if part.startswith("1##"):
                        days["Day 1"] = part[3:].split("##DAY")[0].strip()
                    elif part.startswith("2##"):
                        days["Day 2"] = part[3:].split("##DAY")[0].strip()
                    elif part.startswith("3##"):
                        days["Day 3"] = part[3:].strip()
            else:
                lines = itin.split("\n")
                n = max(len(lines) // 3, 1)
                days["Day 1"] = "\n".join(lines[:n])
                days["Day 2"] = "\n".join(lines[n:2*n])
                days["Day 3"] = "\n".join(lines[2*n:])
            st.session_state.itinerary_days = days

        t1, t2, t3 = st.tabs(["📅 Day 1", "📅 Day 2", "📅 Day 3"])
        with t1:
            st.session_state.itinerary_days["Day 1"] = st.text_area(
                "Edit activities", value=st.session_state.itinerary_days["Day 1"], height=220, key="day1")
        with t2:
            st.session_state.itinerary_days["Day 2"] = st.text_area(
                "Edit activities", value=st.session_state.itinerary_days["Day 2"], height=220, key="day2")
        with t3:
            st.session_state.itinerary_days["Day 3"] = st.text_area(
                "Edit activities", value=st.session_state.itinerary_days["Day 3"], height=220, key="day3")

        if st.button("💾 Save Changes", key="save_itin"):
            st.session_state.itinerary_saved = True
        if st.session_state.get("itinerary_saved"):
            st.markdown('<div style="background:#F0FBF7;border:1px solid #B7E8D4;border-radius:10px;padding:10px 16px;color:#1a8c5b;font-size:13px;font-weight:500;margin-top:8px;font-family:Plus Jakarta Sans,sans-serif">✅ Itinerary saved!</div>', unsafe_allow_html=True)

        card_end()

    with c5:
        card_start("💰", "Full Breakdown", "Expense Dashboard", "#F0F5FF")
        st.write(result["expenses"])
        card_end()

    # Chat
    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="
      background:#fff;border:1px solid #ebebeb;border-radius:20px;
      padding:24px 28px 12px;
    ">
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;padding-bottom:16px;border-bottom:1px solid #f7f7f7;">
        <div style="width:44px;height:44px;background:#FFF0F3;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:20px;">💬</div>
        <div>
          <div style="font-size:17px;font-weight:700;color:#222;font-family:'Plus Jakarta Sans',sans-serif">Ask your travel assistant</div>
          <div style="font-size:13px;color:#717171;font-family:'Plus Jakarta Sans',sans-serif">Visa · packing · budget · local tips</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Ask anything about your trip…")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                response = st.session_state.chat_agent.chat(user_input)
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align:center;padding:40px;color:#bbb;font-size:13px;border-top:1px solid #ebebeb;margin-top:40px;font-family:'Plus Jakarta Sans',sans-serif;">
  Built with Google ADK · MCP · Gemini · RapidAPI &nbsp;·&nbsp; voyager.ai © 2026
</div>
""", unsafe_allow_html=True)
