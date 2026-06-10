import streamlit as st
from utils.constants import APP_TITLE, APP_ICON
from utils.helper import load_css
from dashboard.charts import get_wellness_radar_chart, get_score_gauge
from dashboard.metrics import calculate_overall_metrics

st.set_page_config(page_title=f"Dashboard - {APP_TITLE}", page_icon=APP_ICON, layout="wide")
css = load_css("assets/styles.css")
if css: st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

if not st.session_state.get("initialized"):
    st.warning("Please start from the Home page.")
    st.stop()

st.title("📈 Health Dashboard")

results = st.session_state.assessment_results
metrics = calculate_overall_metrics(results)

if metrics["completed_count"] == 0:
    st.info("You haven't completed any assessments yet. Go to the Health Assessment page to get started!")
    if st.button("Go to Assessments"):
        st.switch_page("pages/2_Health_Assessment.py")
    st.stop()

# ── Top KPIs ──
col1, col2, col3, col4 = st.columns(4)
col1.metric("Assessments Completed", f"{metrics['completed_count']}/{metrics['total_categories']}")
col2.metric("Overall Score", f"{metrics['average_score']}/100")
col3.metric("Profile Status", "Active" if st.session_state.user_name else "Anonymous")
col4.metric("Risk Level", "Low" if metrics['average_score'] > 70 else "Medium" if metrics['average_score'] > 40 else "High")

st.markdown("---")

# ── Charts ──
chart_cols = st.columns([1, 1])

with chart_cols[0]:
    st.subheader("Wellness Balance Radar")
    radar = get_wellness_radar_chart(results)
    if radar:
        st.plotly_chart(radar, use_container_width=True)
    else:
        st.write("Not enough data to display radar chart.")

with chart_cols[1]:
    st.subheader("Category Scores")
    for cat, data in results.items():
        if data:
            st.plotly_chart(get_score_gauge(data["score"], cat.replace("_", " ").title()), use_container_width=True)
