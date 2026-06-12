import streamlit as st
import os
from datetime import datetime
from utils.constants import APP_TITLE, APP_ICON

st.set_page_config(page_title=f"Wellness Report - {APP_TITLE}", page_icon=APP_ICON, layout="wide")

# Load CSS
def load_css():
    css_path = "assets/styles.css"
    if os.path.exists(css_path):
        with open(css_path, encoding='utf-8') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
#load_css()

if not st.session_state.get("initialized"):
    st.warning("⚠️ Please go back to the Home page to initialize the app.")
    st.stop()

st.title("📋 Comprehensive Wellness Report")
st.markdown("Generate and download a complete PDF wellness report containing all your assessment results, AI insights, and recommendations.")

results = st.session_state.assessment_results
completed = sum(1 for v in results.values() if v is not None)

if completed == 0:
    st.warning("⚠️ You must complete at least one health assessment before generating a report.")
    if st.button("Go to Health Assessment"):
        st.switch_page("pages/2_Health_Assessment.py")
    st.stop()

# Show what's completed
st.markdown(f"**{completed}/4 assessments completed:**")
cols = st.columns(4)
cats = {"sleep": "😴 Sleep", "stress": "😰 Stress", "diet": "🥗 Diet", "screen_time": "📱 Screen Time"}
for i, (k, label) in enumerate(cats.items()):
    with cols[i]:
        if results.get(k):
            score = results[k]["score"]
            color = "#00BFA6" if score >= 70 else "#FFB347" if score >= 40 else "#FF6584"
            st.markdown(f"<div style='text-align:center; padding:0.5rem; border-radius:8px; border: 1px solid {color};'>"
                        f"<b>{label}</b><br><span style='color:{color}; font-size:1.3rem; font-weight:700;'>{score}/100</span></div>",
                        unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align:center; padding:0.5rem; border-radius:8px; background:#1A1D23; color:#555;'>"
                        f"<b>{label}</b><br><span>Not done</span></div>", unsafe_allow_html=True)

st.markdown("---")

with st.form("report_form"):
    st.markdown("### 👤 Confirm Your Profile")
    c1, c2, c3 = st.columns(3)
    with c1:
        name = st.text_input("Your Name", value=st.session_state.get("user_name") or "Student")
    with c2:
        age = st.number_input("Your Age", value=int(st.session_state.get("user_age") or 20), min_value=10, max_value=100)
    with c3:
        options = ["School", "College", "Postgrad", "Professional"]
        current = st.session_state.get("student_type", "College")
        if current not in options:
            current = "College"
        student_type = st.selectbox("Student Type", options, index=options.index(current))

    submitted = st.form_submit_button("📄 Generate PDF Report", use_container_width=True)

if submitted:
    st.session_state.user_name = name
    st.session_state.user_age = age
    st.session_state.student_type = student_type

    with st.spinner("🔄 Compiling your wellness data and generating PDF..."):
        try:
            from utils.pdf_generator import generate_pdf_report
            from utils.helper import get_score_status

            # Calculate overall score
            scores = [results[k]["score"] for k in results if results[k]]
            overall_score = round(sum(scores) / len(scores), 1) if scores else 0

            # Build category_scores list
            category_scores = []
            for cat, res in results.items():
                if res:
                    category_scores.append({
                        "category": cat,
                        "score": res.get("score", 0),
                        "status": res.get("status", "Unknown"),
                        "recommendations": [
                            t.get("tip", str(t)) if isinstance(t, dict) else str(t)
                            for t in res.get("tips", [])[:5]
                        ]
                    })

            # Get routine if available
            routine_text = st.session_state.get("current_routine", "")

            # Output filepath
            safe_name = name.replace(" ", "_").replace("/", "-")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"reports/generated_reports/{safe_name}_{timestamp}.pdf"

            generate_pdf_report(
                user_name=name,
                user_age=age,
                student_type=student_type,
                overall_score=overall_score,
                category_scores=category_scores,
                results=results,
                routine_text=routine_text,
                filepath=filepath
            )

            st.session_state.report_filepath = filepath
            st.session_state.report_generated = True
            st.success(f"✅ PDF Report generated successfully! Overall Score: **{overall_score}/100**")

        except Exception as e:
            st.error(f"❌ Error generating report: {str(e)}")
            st.exception(e)

# Download button
if st.session_state.get("report_generated") and st.session_state.get("report_filepath"):
    filepath = st.session_state.report_filepath
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            st.download_button(
                label="⬇️ Download Your PDF Wellness Report",
                data=f,
                file_name=os.path.basename(filepath),
                mime="application/pdf",
                use_container_width=True
            )

        st.markdown("---")

        st.markdown("### 📊 Report Summary")

        for cat, label in cats.items():
            res = results.get(cat)
            if not res:
                continue

            st.subheader(f"{label} — Score: {res['score']}/100")

            st.markdown(f"**Status:** {res.get('status_emoji','')} {res.get('status','')}")

            analysis = res.get("analysis", "")

            if isinstance(analysis, list):
                analysis = " ".join(str(x) for x in analysis)
            else:
                analysis = str(analysis)

            st.markdown(f"**AI Analysis:**\n\n{analysis}")

            tips = res.get("tips", [])
            if tips:
                st.markdown("**Top Tips:**")
                for t in tips[:3]:
                    tip_text = t.get("tip", str(t)) if isinstance(t, dict) else str(t)
                    st.markdown(f"- {tip_text}")

            st.markdown("---")