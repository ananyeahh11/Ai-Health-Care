# 🩺 AI Health Awareness Agent

> **This tool is for awareness only, not medical advice.**

A Streamlit-based AI wellness companion for students that provides safe, general health awareness suggestions around **sleep, stress, diet, and screen time**, powered by Google Gemini API.

---

## 📋 Problem Statement

Students need basic health awareness around sleep, stress, diet, and study-life balance. This AI Health Awareness Agent gives safe, general wellness suggestions while clearly avoiding medical diagnosis.

## ✨ Features

- **😴 Sleep Assessment** — Evaluate sleep patterns and get tips for better rest
- **😰 Stress Assessment** — Understand stress levels with coping strategy suggestions
- **🥗 Diet Assessment** — Review eating habits with nutrition awareness tips
- **📱 Screen Time Assessment** — Analyze digital habits for better screen-life balance
- **💬 AI Chat Assistant** — Ask wellness questions in a conversational interface
- **📋 Daily Routine Generator** — Get a personalized daily schedule
- **📊 Wellness Report** — Download a comprehensive wellness report
- **🛡️ Safety First** — Emergency detection with helpline resources

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI/LLM**: Google Gemini API (`gemini-1.5-flash`)
- **Language**: Python 3.10+
- **Data Validation**: Pydantic
- **Environment**: python-dotenv

## 🚀 Setup & Installation

### 1. Clone / Navigate to the project

```bash
cd "AI Health Awareness Agent"
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API key

1. Get a free API key from [Google AI Studio](https://aistudio.google.com/)
2. Open the `.env` file and replace the placeholder:

```
GOOGLE_API_KEY=your_actual_api_key_here
```

### 5. Run the application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
AI_Health_Awareness_Agent/
├── app.py                  # Main Streamlit app
├── requirements.txt        # Python dependencies
├── .env                    # API key (not committed)
├── README.md               # This file
├── data/                   # Static wellness data
│   ├── wellness_tips.json
│   ├── health_guidelines.json
│   └── routines.json
├── prompts/                # LLM prompt templates
│   ├── system_prompt.txt
│   ├── safety_prompt.txt
│   └── routine_generator_prompt.txt
├── services/               # Business logic
│   ├── llm_service.py
│   ├── health_advisor.py
│   ├── routine_generator.py
│   └── safety_checker.py
├── utils/                  # Utilities
│   ├── validators.py
│   ├── constants.py
│   └── helper.py
├── pages/                  # Streamlit pages
│   ├── sleep_assessment.py
│   ├── stress_assessment.py
│   ├── diet_assessment.py
│   └── screen_time_assessment.py
├── models/                 # Data models
│   ├── user_profile.py
│   └── wellness_report.py
├── static/                 # Static assets
│   ├── logo.png
│   └── styles.css
└── reports/
    └── generated_reports/  # Downloaded reports saved here
```

## ⚠️ Disclaimer

**This tool is for awareness only, not medical advice.** The AI Health Awareness Agent provides general wellness suggestions and does not diagnose medical conditions, prescribe medications, or replace professional healthcare advice. Always consult a qualified healthcare professional for medical concerns.

## 📞 Emergency Resources

If you or someone you know is in crisis:
- **iCall (India)**: 9152987821
- **AASRA (India)**: 9820466726
- **Emergency**: 112
- **Crisis Text Line**: Text HOME to 741741

---

Made with ❤️ for student wellness
