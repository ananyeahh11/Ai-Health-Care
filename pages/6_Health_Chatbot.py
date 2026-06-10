import streamlit as st
import os
from utils.constants import APP_TITLE, APP_ICON

st.set_page_config(page_title=f"AI Chatbot - {APP_TITLE}", page_icon=APP_ICON, layout="wide")

def load_css():
    css_path = "assets/styles.css"
    if os.path.exists(css_path):
        with open(css_path, encoding='utf-8') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css()

if not st.session_state.get("initialized"):
    st.warning("Please go back to the Home page to initialize the app.")
    st.stop()

llm = st.session_state.llm_service
safety = st.session_state.safety_checker

# ── Fallback tips shown when API is rate-limited ──────────────────────────────
FALLBACK_TIPS = {
    "😴 Better Sleep Tips": [
        "**Stick to a schedule:** Go to bed and wake up at the same time every day, even on weekends.",
        "**Avoid screens 30 min before bed:** Blue light from phones suppresses melatonin and delays sleep.",
        "**Keep your room cool and dark:** A temperature of 18-20°C and darkness signal your body it's time to sleep.",
    ],
    "😌 Reduce Stress": [
        "**Try box breathing:** Inhale for 4 sec, hold 4 sec, exhale 4 sec, hold 4 sec. Repeat 3 times to calm instantly.",
        "**Break tasks into small steps:** Instead of 'study for exam', write 'read chapter 1 for 25 min'. Smaller tasks feel less overwhelming.",
        "**Move your body daily:** Even a 15-minute walk releases endorphins that directly reduce stress hormones.",
    ],
    "🥗 Healthy Eating Habits": [
        "**Never skip breakfast:** It kick-starts your metabolism and improves concentration for morning classes.",
        "**Carry a water bottle:** Most students mistake thirst for hunger. Staying hydrated also improves focus.",
        "**Prep one healthy snack daily:** Fruits, nuts, or yogurt are quick options that prevent junk food cravings.",
    ],
    "📱 Reduce Screen Time": [
        "**Use the 20-20-20 rule:** Every 20 minutes, look at something 20 feet away for 20 seconds to reduce eye strain.",
        "**Set app timers:** Use your phone's built-in screen time/digital wellbeing tool to set daily limits on social media.",
        "**Phone-free zones:** Keep your phone out of the bedroom and off the dining table to naturally reduce usage.",
    ],
    "📚 Study-Life Balance": [
        "**Use time blocking:** Assign specific hours for studying, rest, and social time. Treat each block like a class.",
        "**Take a proper break every 45-50 min:** Short breaks (Pomodoro technique) improve retention and prevent burnout.",
        "**Schedule fun too:** Put social activities and hobbies in your calendar — they're not optional extras, they're essential.",
    ],
    "🧘 Mindfulness & Relaxation": [
        "**Start with 5 minutes:** Download a free app (Calm, Headspace) and commit to just 5 minutes of guided meditation daily.",
        "**Try progressive muscle relaxation:** Tense and release each muscle group from toes to head — very effective before exams.",
        "**Spend time in nature:** Even a 10-minute walk outside lowers cortisol (the stress hormone) significantly.",
    ],
}

# ── LLM prompts (short — 2-3 tips only) ──────────────────────────────────────
QUICK_PROMPTS = {
    "😴 Better Sleep Tips": (
        "Give exactly 3 concise, practical sleep improvement tips for a student. "
        "Format each as: **Tip title:** One sentence explanation. Keep each tip under 30 words."
    ),
    "😌 Reduce Stress": (
        "Give exactly 3 concise stress management tips for a student. "
        "Format each as: **Tip title:** One sentence explanation. Keep each tip under 30 words."
    ),
    "🥗 Healthy Eating Habits": (
        "Give exactly 3 concise healthy eating tips for a student. "
        "Format each as: **Tip title:** One sentence explanation. Keep each tip under 30 words."
    ),
    "📱 Reduce Screen Time": (
        "Give exactly 3 concise tips to reduce screen time for a student. "
        "Format each as: **Tip title:** One sentence explanation. Keep each tip under 30 words."
    ),
    "📚 Study-Life Balance": (
        "Give exactly 3 concise study-life balance tips for a student. "
        "Format each as: **Tip title:** One sentence explanation. Keep each tip under 30 words."
    ),
    "🧘 Mindfulness & Relaxation": (
        "Give exactly 3 concise mindfulness tips for a student. "
        "Format each as: **Tip title:** One sentence explanation. Keep each tip under 30 words."
    ),
}

ERROR_PHRASES = [
    "high demand", "try again", "encountered an issue", "unable to generate",
    "api key error", "internet connection"
]

def is_error_response(text):
    lower = text.lower()
    return any(phrase in lower for phrase in ERROR_PHRASES)

def format_fallback(tips):
    return "\n\n".join([f"{i+1}. {tip}" for i, tip in enumerate(tips)])


# ── Page Header ───────────────────────────────────────────────────────────────
st.title("💬 AI Health Awareness Chatbot")
st.markdown("Get safe, general wellness tips on sleep, stress, diet, and more.")

# ── Quick Action Buttons ──────────────────────────────────────────────────────
st.markdown("### ⚡ Quick Tips — click any topic:")
topic_keys = list(QUICK_PROMPTS.keys())
row1 = st.columns(3)
row2 = st.columns(3)

for i, col in enumerate(row1):
    with col:
        if st.button(topic_keys[i], key=f"qa_{i}", use_container_width=True):
            st.session_state.pending_quick_topic = topic_keys[i]

for i, col in enumerate(row2):
    idx = i + 3
    if idx < len(topic_keys):
        with col:
            if st.button(topic_keys[idx], key=f"qa_{idx}", use_container_width=True):
                st.session_state.pending_quick_topic = topic_keys[idx]

# Handle quick topic button press
if st.session_state.get("pending_quick_topic"):
    topic = st.session_state.pending_quick_topic
    display_msg = f"Give me tips on: {topic}"

    st.session_state.chat_history.append({"role": "user", "content": display_msg})

    with st.spinner("Getting tips..."):
        try:
            response = llm.generate_response(QUICK_PROMPTS[topic])
            _, cleaned = safety.check_ai_output(response)
            # If LLM is rate-limited or errors, fall back to pre-written tips
            if is_error_response(cleaned):
                cleaned = format_fallback(FALLBACK_TIPS.get(topic, ["No tips available."]))
        except Exception:
            cleaned = format_fallback(FALLBACK_TIPS.get(topic, ["No tips available."]))

    st.session_state.chat_history.append({"role": "assistant", "content": cleaned})
    del st.session_state.pending_quick_topic
    st.rerun()

st.markdown("---")

# ── Chat History ──────────────────────────────────────────────────────────────
if not st.session_state.chat_history:
    st.markdown("""
    <div style='text-align:center; padding:3rem 1rem; color:#555;'>
        <div style='font-size:3rem;'>💬</div>
        <p style='font-size:1.1rem;'>Click a topic above or type your question below!</p>
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

# ── Free Chat Input ───────────────────────────────────────────────────────────
if prompt := st.chat_input("Type your health question..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    is_safe, safety_response = safety.check_user_input(prompt)
    if not is_safe:
        with st.chat_message("assistant"):
            st.markdown(safety_response)
        st.session_state.chat_history.append({"role": "assistant", "content": safety_response})
    elif safety.is_medical_query(prompt):
        redirect = safety.get_medical_redirect_response()
        with st.chat_message("assistant"):
            st.markdown(redirect)
        st.session_state.chat_history.append({"role": "assistant", "content": redirect})
    else:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                history = [
                    {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
                    for m in st.session_state.chat_history[:-1]
                ]
                try:
                    response = llm.generate_response(prompt, history)
                    _, cleaned = safety.check_ai_output(response)
                    if is_error_response(cleaned):
                        cleaned = "I'm having trouble right now. Please try again in a moment, or click one of the quick topic buttons above for instant tips."
                except Exception:
                    cleaned = "Please try again in a moment, or click a quick topic button above."
                st.markdown(cleaned)
        st.session_state.chat_history.append({"role": "assistant", "content": cleaned})
