import streamlit as st
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.constants import APP_TITLE, APP_ICON

# ── Page config (must be FIRST) ──────────────────────────────────────────────
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Load CSS ──────────────────────────────────────────────────────────────────
def load_css():
    css_path = "assets/styles.css"
    if os.path.exists(css_path):
        with open(css_path, encoding='utf-8') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()


# ── Session State Init ────────────────────────────────────────────────────────
def init_session_state():
    defaults = {
        "initialized": False,
        "chat_history": [],
        "assessment_results": {
            "sleep": None, "stress": None,
            "diet": None, "screen_time": None
        },
        "user_name": "",
        "user_age": 20,
        "student_type": "College",
        "service_error": None,
        "current_routine": None,
        "report_data": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def init_services():
    if st.session_state.initialized:
        return
    try:
        from services.llm_service import LLMService
        from services.health_advisor import HealthAdvisor
        from services.routine_generator import RoutineGenerator
        from services.safety_checker import SafetyChecker

        llm = LLMService()
        st.session_state.llm_service = llm
        st.session_state.health_advisor = HealthAdvisor(llm)
        st.session_state.routine_generator = RoutineGenerator(llm)
        st.session_state.safety_checker = SafetyChecker()
        st.session_state.service_error = None
        st.session_state.initialized = True
    except Exception as e:
        st.session_state.service_error = str(e)
        st.session_state.initialized = False

init_session_state()
init_services()

# ── Navigation (hides app.py from sidebar) ────────────────────────────────────
pg = st.navigation([
    st.Page("pages/1_Home.py",              title="🏠 Home",                 default=True),
    st.Page("pages/2_Health_Assessment.py", title="🏥 Health Assessment"),
    st.Page("pages/3_Dashboard.py", title="📊 Dashboard"),
    st.Page("pages/4_Daily_Routine.py",     title="📅 Daily Routine"),
    st.Page("pages/5_Wellness_Report.py", title="📄 Wellness Report"),
    st.Page("pages/6_Health_Chatbot.py",    title="💬 AI Chatbot"),
    st.Page("pages/7_Emergency_Guide.py",   title="🛡️ Emergency Guide"),
])

# Service error banner
if st.session_state.service_error:
    st.sidebar.error(f"⚠️ Service error: {st.session_state.service_error[:120]}")

pg.run()
