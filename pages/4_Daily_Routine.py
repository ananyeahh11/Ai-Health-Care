import streamlit as st
from utils.constants import APP_TITLE, APP_ICON
from utils.helper import load_css

st.set_page_config(page_title=f"Routine Generator - {APP_TITLE}", page_icon=APP_ICON, layout="wide")
css = load_css("assets/styles.css")
if css: st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

if not st.session_state.get("initialized"):
    st.warning("Please start from the Home page.")
    st.stop()

st.title("📅 Daily Routine Generator")
st.markdown("Generate a personalized daily schedule that balances academics with your health assessment results.")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### Preferences")
    wake_time = st.time_input("Wake-up time", value=None)
    routine_type = st.selectbox("Routine Focus", ["Balanced", "Exam Preparation", "Relaxation / Weekend"])
    energy_levels = st.selectbox("When are you most productive?", ["Morning", "Afternoon", "Night"])
    
    if st.button("Generate Routine", use_container_width=True):
        if not wake_time:
            st.error("Please select a wake-up time.")
        else:
            with st.spinner("Creating your personalized routine..."):
                routine = st.session_state.routine_generator.generate_routine(
                    user_data=st.session_state.assessment_results,
                    preferences={
                        "wake_time": str(wake_time),
                        "routine_type": routine_type,
                        "user_name": st.session_state.user_name
                    }
                )
                st.session_state.current_routine = routine

with col2:
    if "current_routine" in st.session_state:
        st.markdown("### Your Personalized Schedule")
        st.markdown(st.session_state.current_routine)
    else:
        st.info("Fill out your preferences on the left and click 'Generate Routine' to see your schedule.")
