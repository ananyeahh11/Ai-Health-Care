import streamlit as st
import os
from utils.constants import APP_TITLE, APP_ICON

st.set_page_config(page_title=f"Health Assessment - {APP_TITLE}", page_icon=APP_ICON, layout="wide")

def load_css():
    css_path = "assets/styles.css"
    if os.path.exists(css_path):
        with open(css_path, encoding='utf-8') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css()

if not st.session_state.get("initialized"):
    st.warning("Please go back to the Home page to initialize the app.")
    st.stop()

advisor = st.session_state.health_advisor

def show_score_card(score, status, emoji, color):
    st.markdown(f"""
    <div style='text-align:center; padding:1.2rem; border-radius:14px;
         background: linear-gradient(145deg,#1A1D23,#22262E); border:2px solid {color}; margin:0.5rem 0;'>
        <div style='font-size:2.5rem; font-weight:800; color:{color};'>{score}<span style='font-size:1rem;'>/100</span></div>
        <div style='font-size:1rem; color:#A0AEC0;'>{emoji} {status}</div>
    </div>
    """, unsafe_allow_html=True)

def show_awareness_rules(category):
    rules = {
        "sleep": [
            "🌙 Adults need 7–9 hours of sleep per night for optimal health.",
            "📵 Avoid screens (phones, laptops) 30–60 minutes before bed.",
            "☕ Limit caffeine intake after 2 PM to improve sleep quality.",
            "🛏️ Keep your bedroom cool, dark, and quiet for better rest.",
            "⏰ Maintain a consistent sleep and wake time even on weekends.",
        ],
        "stress": [
            "🧘 Practice 5–10 minutes of deep breathing or meditation daily.",
            "🏃 Regular exercise (30 min, 3–5×/week) significantly reduces stress.",
            "💬 Talk to a trusted friend, family member, or counsellor.",
            "📓 Journaling helps identify and process stress triggers.",
            "🎯 Break large tasks into small steps to avoid feeling overwhelmed.",
        ],
        "diet": [
            "🥗 Aim for 5+ servings of fruits and vegetables daily.",
            "💧 Drink 8–10 glasses of water per day to stay hydrated.",
            "🍳 Never skip breakfast — it fuels your brain for the day.",
            "🚫 Limit junk food, sugary drinks, and late-night eating.",
            "🕑 Eat meals at regular times to stabilise your energy levels.",
        ],
        "screen_time": [
            "👁️ Follow the 20-20-20 rule: every 20 min, look 20 ft away for 20 sec.",
            "⏸️ Take a 5-minute break every 45–60 minutes of continuous screen use.",
            "📱 Limit recreational social media to 1–2 hours per day.",
            "🌙 No screens in bed — it disrupts your sleep hormone (melatonin).",
            "🖥️ Adjust screen brightness and use night mode in the evening.",
        ]
    }
    st.markdown("#### 📚 General Health Awareness Rules")
    for rule in rules.get(category, []):
        st.markdown(f"<div style='padding:0.4rem 0.8rem; margin:0.3rem 0; border-left:3px solid #6C63FF; "
                    f"background:#1A1D23; border-radius:0 8px 8px 0; font-size:0.92rem;'>{rule}</div>",
                    unsafe_allow_html=True)

def show_improvement_tips(result, category):
    st.markdown("#### 💡 How to Improve Your Routine")
    improvements = {
        "sleep": {
            "low": ["Start by going to bed 30 minutes earlier each week",
                    "Create a relaxing pre-sleep routine (reading, light stretching)",
                    "Put your phone face-down or in another room 1 hour before sleep",
                    "Use blackout curtains and keep the room below 20°C"],
            "mid": ["Fine-tune your sleep environment (noise, temperature, light)",
                    "Try a 10-minute mindfulness session before bed",
                    "Avoid large meals within 2 hours of bedtime"],
            "high": ["Maintain your current schedule consistently",
                     "Track your sleep quality weekly to notice any dips",
                     "Share your sleep tips with friends!"]
        },
        "stress": {
            "low": ["Start a simple 5-min morning meditation using a free app",
                    "Write down 3 things you're grateful for each evening",
                    "Speak with your college counsellor or a trusted mentor",
                    "Break your study sessions into 45-min blocks with 10-min breaks"],
            "mid": ["Add one new stress-relief activity this week (yoga, walking)",
                    "Plan your week on Sunday to reduce decision fatigue",
                    "Reduce news and social media to 30 min/day"],
            "high": ["Continue your positive coping strategies",
                     "Help peers who may be struggling with stress",
                     "Set new personal growth goals now that stress is managed"]
        },
        "diet": {
            "low": ["Prep healthy snacks (fruits, nuts) at the start of each week",
                    "Start every meal with a glass of water",
                    "Add one vegetable or fruit to each meal this week",
                    "Cook or order one healthy meal per day as a starting habit"],
            "mid": ["Plan your meals for the week ahead on Sundays",
                    "Reduce one unhealthy habit at a time (e.g., skip one junk meal)",
                    "Try adding protein (eggs, legumes) to your breakfast"],
            "high": ["Explore new healthy recipes to keep meals interesting",
                     "Try intermittent fasting or mindful eating experiments",
                     "Stay consistent — nutrition is a long-term investment"]
        },
        "screen_time": {
            "low": ["Set app timers on Instagram/YouTube to 30 min/day",
                    "Designate 'phone-free' zones: dining table, bedroom at night",
                    "Replace 1 hour of scrolling with a walk or physical activity",
                    "Use Grayscale mode on your phone to make it less appealing"],
            "mid": ["Set a hard stop for screens at 9:30 PM every night",
                    "Use website blockers during study hours",
                    "Try one digital detox day per month"],
            "high": ["Your screen habits are excellent — keep it up!",
                     "Consider sharing your strategies with classmates",
                     "Stay mindful as workload increases during exams"]
        }
    }

    score = result.get("score", 0)
    level = "low" if score < 40 else "mid" if score < 70 else "high"
    tips_list = improvements.get(category, {}).get(level, [])
    for tip in tips_list:
        st.markdown(f"<div style='padding:0.4rem 0.8rem; margin:0.3rem 0; border-left:3px solid #00BFA6; "
                    f"background:#0D1F1A; border-radius:0 8px 8px 0; font-size:0.92rem;'>{tip}</div>",
                    unsafe_allow_html=True)


# ── Page Header ──────────────────────────────────────────────────────────────
st.title("🏥 AI Health Assessment")
st.markdown("Complete each section to receive personalized wellness scores, AI-powered suggestions, and improvement guidance.")
st.markdown("---")

# ── User Profile Section ──────────────────────────────────────────────────────
st.markdown("""
<div style='background:#1A1D23; border:1px solid #2D2D2D; border-radius:12px;
     padding:1rem 1.5rem; margin-bottom:1rem;'>
    <h4 style='color:#6C63FF; margin:0 0 0.5rem 0;'>👤 Your Profile — helps personalize AI suggestions</h4>
</div>
""", unsafe_allow_html=True)

with st.container():
    c1, c2, c3 = st.columns(3)
    with c1:
        name = st.text_input("Your Name", value=st.session_state.get("user_name", ""), placeholder="e.g. Priya")
        if name: st.session_state.user_name = name
    with c2:
        age = st.number_input("Your Age", 10, 60, value=int(st.session_state.get("user_age", 20)))
        st.session_state.user_age = age
    with c3:
        opts = ["School", "College", "Postgrad", "Professional"]
        stype = st.selectbox("Student Type", opts)
        st.session_state.student_type = stype

tabs = st.tabs(["😴 Sleep", "😰 Stress", "🥗 Diet & Nutrition", "📱 Screen Time"])

# ══════════════════════════════════════════════════════════════════════
# SLEEP TAB
# ══════════════════════════════════════════════════════════════════════
with tabs[0]:
    col_form, col_rules = st.columns([1, 1])

    with col_form:
        st.subheader("Sleep Quality Assessment")
        with st.form("sleep_form"):
            hours = st.slider("Average hours of sleep per night", 0.0, 12.0, 7.0, 0.5,
                              help="7–9 hours is recommended for students")
            quality = st.slider("Rate your sleep quality (1=very poor, 10=excellent)", 1, 10, 5)
            env_quality = st.slider("Sleep environment quality (noise, light, temperature)", 1, 10, 5)
            naps = st.radio("Do you take daytime naps?", ["Yes", "No"]) == "Yes"
            caffeine = st.radio("Do you drink caffeine after 2 PM?", ["Yes", "No"]) == "Yes"
            screen_before_bed = st.radio("Do you use screens 30 min before sleep?", ["Yes", "No"]) == "Yes"
            analyze_sleep = st.form_submit_button("🔍 Analyze My Sleep", use_container_width=True)

        if analyze_sleep:
            with st.spinner("Analyzing your sleep patterns with AI..."):
                result = advisor.assess_sleep({
                    "hours": hours, "quality": quality, "environment_quality": env_quality,
                    "naps": naps, "caffeine_after_2pm": caffeine,
                    "screen_before_bed": screen_before_bed
                })
                st.session_state.assessment_results["sleep"] = result

    with col_rules:
        show_awareness_rules("sleep")

    # Results (full width below)
    if st.session_state.assessment_results.get("sleep"):
        res = st.session_state.assessment_results["sleep"]
        st.markdown("---")
        r1, r2 = st.columns([1, 2])
        with r1:
            show_score_card(res['score'], res['status'], res.get('status_emoji',''), res['status_color'])
            if res.get("consult_doctor"):
                st.warning("⚠️ Your sleep patterns suggest you should speak with a healthcare professional.")
        with r2:
            st.markdown("#### 🤖 AI Wellness Analysis")
            st.markdown(res.get('analysis', ''))
        st.markdown("---")
        show_improvement_tips(res, "sleep")
        if res.get("tips"):
            st.markdown("#### 🏷️ Personalized Tips")
            for tip in res["tips"]:
                t = tip.get("tip", str(tip)) if isinstance(tip, dict) else str(tip)
                st.markdown(f"✅ {t}")

# ══════════════════════════════════════════════════════════════════════
# STRESS TAB
# ══════════════════════════════════════════════════════════════════════
with tabs[1]:
    col_form, col_rules = st.columns([1, 1])

    with col_form:
        st.subheader("Stress & Mental Wellbeing Assessment")
        with st.form("stress_form"):
            level = st.slider("Current stress level (1=very relaxed, 10=extremely stressed)", 1, 10, 5)
            overwhelm = st.selectbox("How often do you feel overwhelmed?",
                                     ["Never", "Rarely", "Once a week", "A few times a week", "Almost every day"])
            exercise = st.selectbox("How often do you exercise?",
                                    ["Never", "Rarely", "Once a week", "2-3 times a week", "4-5 times a week", "Daily"])
            coping = st.multiselect("What are your coping strategies?",
                                    ["Exercise / Sports", "Talking to friends/family",
                                     "Meditation / Deep breathing", "Journaling",
                                     "Listening to music", "Watching shows / Gaming",
                                     "Sleeping", "Nothing specific"])
            analyze_stress = st.form_submit_button("🔍 Analyze My Stress", use_container_width=True)

        if analyze_stress:
            with st.spinner("Analyzing your stress levels with AI..."):
                result = advisor.assess_stress({
                    "level": level, "overwhelm_frequency": overwhelm,
                    "exercise_frequency": exercise, "coping_mechanisms": coping
                })
                st.session_state.assessment_results["stress"] = result

    with col_rules:
        show_awareness_rules("stress")

    if st.session_state.assessment_results.get("stress"):
        res = st.session_state.assessment_results["stress"]
        st.markdown("---")
        r1, r2 = st.columns([1, 2])
        with r1:
            show_score_card(res['score'], res['status'], res.get('status_emoji',''), res['status_color'])
            if res.get("consult_doctor"):
                st.error("⚠️ Your stress level is high. Please consider speaking to a mental health professional.")
        with r2:
            st.markdown("#### 🤖 AI Wellness Analysis")
            st.markdown(res.get('analysis', ''))
        st.markdown("---")
        show_improvement_tips(res, "stress")
        if res.get("tips"):
            st.markdown("#### 🏷️ Personalized Tips")
            for tip in res["tips"]:
                t = tip.get("tip", str(tip)) if isinstance(tip, dict) else str(tip)
                st.markdown(f"✅ {t}")

# ══════════════════════════════════════════════════════════════════════
# DIET TAB
# ══════════════════════════════════════════════════════════════════════
with tabs[2]:
    col_form, col_rules = st.columns([1, 1])

    with col_form:
        st.subheader("Diet & Nutrition Assessment")
        with st.form("diet_form"):
            meals = st.slider("How many meals do you eat per day?", 1, 6, 3)
            water = st.slider("Glasses of water per day", 0, 15, 6)
            fruit_veg = st.slider("Servings of fruits & vegetables per day", 0, 10, 2)
            skips_bf = st.radio("Do you skip breakfast?", ["Yes", "No"]) == "Yes"
            junk = st.selectbox("How often do you eat junk food?",
                                ["Never", "Rarely", "Once a week", "A few times a week", "Daily"])
            late_night = st.radio("Do you eat late at night (after 9 PM)?", ["Yes", "No"]) == "Yes"
            analyze_diet = st.form_submit_button("🔍 Analyze My Diet", use_container_width=True)

        if analyze_diet:
            with st.spinner("Analyzing your diet habits with AI..."):
                result = advisor.assess_diet({
                    "meals_per_day": meals, "water_glasses": water,
                    "fruit_veg_servings": fruit_veg, "skips_breakfast": skips_bf,
                    "junk_food_frequency": junk, "late_night_eating": late_night
                })
                st.session_state.assessment_results["diet"] = result

    with col_rules:
        show_awareness_rules("diet")

    if st.session_state.assessment_results.get("diet"):
        res = st.session_state.assessment_results["diet"]
        st.markdown("---")
        r1, r2 = st.columns([1, 2])
        with r1:
            show_score_card(res['score'], res['status'], res.get('status_emoji',''), res['status_color'])
        with r2:
            st.markdown("#### 🤖 AI Wellness Analysis")
            st.markdown(res.get('analysis', ''))
        st.markdown("---")
        show_improvement_tips(res, "diet")
        if res.get("tips"):
            st.markdown("#### 🏷️ Personalized Tips")
            for tip in res["tips"]:
                t = tip.get("tip", str(tip)) if isinstance(tip, dict) else str(tip)
                st.markdown(f"✅ {t}")

# ══════════════════════════════════════════════════════════════════════
# SCREEN TIME TAB
# ══════════════════════════════════════════════════════════════════════
with tabs[3]:
    col_form, col_rules = st.columns([1, 1])

    with col_form:
        st.subheader("Screen Time & Digital Wellness Assessment")
        with st.form("screen_time_form"):
            daily_hours = st.slider("Total daily screen hours (excluding academics)", 0, 16, 6)
            social = st.slider("Hours spent on social media daily", 0, 10, 2)
            breaks = st.radio("Do you take regular screen breaks?", ["Yes", "No"]) == "Yes"
            break_freq = st.selectbox("How often do you take breaks?",
                                      ["Every 20 minutes", "Every 30 minutes", "Every hour",
                                       "Every 2 hours", "Rarely take breaks"])
            before_bed = st.radio("Do you use screens right before bed?", ["Yes", "No"]) == "Yes"
            eye_strain = st.radio("Do you experience eye strain or headaches?", ["Yes", "No"]) == "Yes"
            analyze_screen = st.form_submit_button("🔍 Analyze My Screen Time", use_container_width=True)

        if analyze_screen:
            with st.spinner("Analyzing your screen habits with AI..."):
                result = advisor.assess_screen_time({
                    "daily_hours": daily_hours, "social_media_hours": social,
                    "takes_breaks": breaks, "break_frequency": break_freq,
                    "screen_before_bed": before_bed, "eye_strain": eye_strain
                })
                st.session_state.assessment_results["screen_time"] = result

    with col_rules:
        show_awareness_rules("screen_time")

    if st.session_state.assessment_results.get("screen_time"):
        res = st.session_state.assessment_results["screen_time"]
        st.markdown("---")
        r1, r2 = st.columns([1, 2])
        with r1:
            show_score_card(res['score'], res['status'], res.get('status_emoji',''), res['status_color'])
            if res.get("consult_doctor"):
                st.warning("⚠️ Consider consulting an eye specialist if eye strain persists.")
        with r2:
            st.markdown("#### 🤖 AI Wellness Analysis")
            st.markdown(res.get('analysis', ''))
        st.markdown("---")
        show_improvement_tips(res, "screen_time")
        if res.get("tips"):
            st.markdown("#### 🏷️ Personalized Tips")
            for tip in res["tips"]:
                t = tip.get("tip", str(tip)) if isinstance(tip, dict) else str(tip)
                st.markdown(f"✅ {t}")

# ── Bottom CTA ───────────────────────────────────────────────────────────────
st.markdown("---")
completed = sum(1 for v in st.session_state.assessment_results.values() if v)
if completed > 0:
    st.success(f"✅ {completed}/4 assessments completed.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📅 Generate My Daily Routine", use_container_width=True):
            st.switch_page("pages/4_Daily_Routine.py")
    with col2:
        if st.button("📋 Generate Wellness Report PDF", use_container_width=True):
            st.switch_page("pages/5_Wellness_Report.py")
