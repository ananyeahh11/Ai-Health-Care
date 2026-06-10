import streamlit as st
import os
from utils.constants import APP_TITLE, APP_ICON, APP_DESCRIPTION, DISCLAIMER_TEXT
from utils.helper import load_css

st.set_page_config(page_title=f"Home - {APP_TITLE}", page_icon=APP_ICON, layout="wide")

# Load CSS
css = load_css("assets/styles.css")
if css:
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# ── Hero Section ──
st.markdown(f"""
    <div style='text-align: center; padding: 3rem 1rem;'>
        <h1 style='font-size: 3.5rem; color: #00BFA6;'>{APP_ICON} {APP_TITLE}</h1>
        <p style='font-size: 1.3rem; color: #A0AEC0; max-width: 800px; margin: 0 auto;'>{APP_DESCRIPTION}</p>
    </div>
""", unsafe_allow_html=True)

# Disclaimer
st.markdown(f'<div class="disclaimer-banner" style="text-align: center;"><strong>⚠️ Important:</strong> {DISCLAIMER_TEXT}</div><br>', unsafe_allow_html=True)

# ── Navigation Cards (Features) ──
st.markdown("### 🌟 Explore Features")
cols = st.columns(3)

with cols[0]:
    st.markdown("""
    <div class='category-card'>
        <h3>📊 Health Assessment</h3>
        <p>Evaluate your Sleep, Stress, Diet, and Screen Time with personalized scoring.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Assessment", key="btn_assess", use_container_width=True):
        st.switch_page("pages/2_Health_Assessment.py")

with cols[1]:
    st.markdown("""
    <div class='category-card'>
        <h3>💬 AI Wellness Assistant</h3>
        <p>Chat with our AI companion to receive safe, general wellness advice.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Chatbot", key="btn_chat", use_container_width=True):
        st.switch_page("pages/6_Health_Chatbot.py")

with cols[2]:
    st.markdown("""
    <div class='category-card'>
        <h3>📅 Daily Routine Generator</h3>
        <p>Get a personalized schedule to balance your study and lifestyle habits.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Create Routine", key="btn_routine", use_container_width=True):
        st.switch_page("pages/4_Daily_Routine.py")

st.markdown("---")

# ── About Us ──
st.markdown("### 🏥 About Us")
st.write("We believe student wellness is the foundation of academic success. Our AI Health Care platform provides you with the basic health awareness you need around sleep, stress, diet, and study-life balance. We aim to guide you toward healthier daily habits using intelligent, non-medical assessments.")

# ── Contact / Footer ──
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p><strong>{APP_TITLE}</strong> — Empowering students with wellness awareness</p>
    <p style="font-size: 0.85rem;">Contact: support@aihealthcare.edu | Follow us for more tips!</p>
</div>
""", unsafe_allow_html=True)
