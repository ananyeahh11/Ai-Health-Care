import streamlit as st
from utils.constants import APP_TITLE, APP_ICON
from utils.helper import load_css

st.set_page_config(page_title=f"Emergency Guide - {APP_TITLE}", page_icon=APP_ICON, layout="wide")
css = load_css("assets/styles.css")
if css: st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

st.title("🛡️ Emergency Awareness Guide")

st.markdown("""
<div class="result-card" style="border-left: 5px solid #FF6584;">
    <h2 style="color: #FF6584;">⚠️ Critical Medical Disclaimer</h2>
    <p style="font-size: 1.1rem;">
        The AI Health Care platform is designed for <b>educational and general wellness awareness purposes only.</b> 
        It is NOT a substitute for professional medical advice, diagnosis, or treatment. 
    </p>
    <p>
        Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition. 
        Never disregard professional medical advice or delay in seeking it because of something you have read on this platform.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.header("📞 Immediate Help Resources")
st.markdown("If you think you may have a medical emergency, call your doctor, go to the nearest hospital emergency department, or call emergency services immediately.")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🚑 Emergency Services")
    st.info("**National Emergency Number:** 112 (India) / 911 (US) / 999 (UK)")
    st.info("**Ambulance:** 108 (India)")

with col2:
    st.markdown("### 🧠 Mental Health Helplines (India)")
    st.info("**iCall (TISS):** 9152987821")
    st.info("**AASRA:** 9820466726")
    st.info("**Kiran (Mental Health Helpline):** 1800-599-0019")

st.markdown("---")
st.markdown("""
### When to seek immediate medical attention:
*   Difficulty breathing or shortness of breath
*   Chest pain or pressure
*   New confusion or inability to arouse
*   Bluish lips or face
*   Severe, persistent pain
*   Sudden weakness or numbness in the face, arm, or leg
*   Thoughts of self-harm or suicide
""")
