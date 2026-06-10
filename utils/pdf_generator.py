import os
from fpdf import FPDF
from datetime import datetime


def safe_text(text):
    """Convert text to latin-1 safe string."""
    if not isinstance(text, str):
        text = str(text)
    return text.encode('latin-1', 'replace').decode('latin-1')


class WellnessPDF(FPDF):
    def __init__(self, user_name="Student"):
        super().__init__()
        self.user_name = user_name

    def header(self):
        # Background bar
        self.set_fill_color(15, 23, 42)
        self.rect(0, 0, 210, 25, 'F')

        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(0, 191, 166)
        self.cell(0, 15, 'AI Health Awareness Agent - Wellness Report', align='C', ln=True)

        self.set_font('Helvetica', '', 9)
        self.set_text_color(160, 174, 192)
        self.cell(0, 8, f'Generated: {datetime.now().strftime("%d %B %Y, %I:%M %p")}', align='C', ln=True)

        self.set_draw_color(0, 191, 166)
        self.set_line_width(0.5)
        self.line(10, 27, 200, 27)
        self.ln(5)

    def footer(self):
        self.set_y(-20)
        self.set_draw_color(200, 200, 200)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(2)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 5,
                  'DISCLAIMER: This report is for general wellness awareness only. It is NOT medical advice. '
                  'Consult a qualified doctor for medical concerns.',
                  align='C', ln=True)
        self.cell(0, 5, f'Page {self.page_no()}', align='C')

    def section_title(self, title, color=(108, 99, 255)):
        self.set_fill_color(*color)
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 12)
        self.cell(0, 9, f'  {safe_text(title)}', fill=True, ln=True, border=0)
        self.ln(2)
        self.set_text_color(30, 30, 30)

    def score_badge(self, label, score, status):
        colors = {
            'Good': (0, 191, 166),
            'Moderate': (255, 179, 71),
            'Needs Attention': (255, 101, 132),
        }
        color = colors.get(status, (100, 100, 100))
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(50, 50, 50)
        self.cell(80, 8, safe_text(label), ln=False)
        self.set_fill_color(*color)
        self.set_text_color(255, 255, 255)
        self.cell(30, 8, f'{score}/100', fill=True, align='C', ln=False)
        self.set_text_color(50, 50, 50)
        self.set_font('Helvetica', '', 10)
        self.cell(50, 8, f'  Status: {safe_text(status)}', ln=True)
        self.ln(1)

    def bullet_list(self, items, color=(80, 80, 80)):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(*color)
        for item in items:
            text = '  -  ' + safe_text(str(item))
            self.set_x(self.l_margin)
            self.multi_cell(0, 6, text)
        self.ln(1)

    def body_text(self, text, size=10):
        self.set_font('Helvetica', '', size)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 6, safe_text(text))
        self.ln(2)


def generate_pdf_report(user_name, user_age, student_type, overall_score,
                        category_scores, results, routine_text, filepath):
    """
    Generate a full wellness PDF report.

    Args:
        user_name: Name of the user.
        user_age: Age of the user.
        student_type: Type of student.
        overall_score: Computed average score.
        category_scores: List of dicts with score data per category.
        results: Full assessment_results dict from session_state.
        routine_text: Daily routine text if available.
        filepath: Output PDF path.
    """
    # Ensure output directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    pdf = WellnessPDF(user_name=user_name)
    pdf.set_auto_page_break(auto=True, margin=25)
    pdf.add_page()
    pdf.set_text_color(30, 30, 30)

    # ── User Profile ──────────────────────────────────────────────────────────
    pdf.section_title('1. User Profile', color=(108, 99, 255))
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(50, 8, 'Name:', ln=False)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 8, safe_text(user_name), ln=True)

    pdf.set_font('Helvetica', '', 11)
    pdf.cell(50, 8, 'Age:', ln=False)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 8, str(user_age), ln=True)

    pdf.set_font('Helvetica', '', 11)
    pdf.cell(50, 8, 'Student Type:', ln=False)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 8, safe_text(student_type), ln=True)
    pdf.ln(4)

    # ── Overall Wellness Score ────────────────────────────────────────────────
    pdf.section_title('2. Overall Wellness Score', color=(0, 150, 120))
    if overall_score >= 70:
        badge_color = (0, 191, 166)
        verdict = 'Good - Keep up the great work!'
    elif overall_score >= 40:
        badge_color = (255, 179, 71)
        verdict = 'Moderate - Room for improvement.'
    else:
        badge_color = (255, 101, 132)
        verdict = 'Needs Attention - Focus on wellness now.'

    pdf.set_fill_color(*badge_color)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 20)
    pdf.cell(0, 14, f'Overall Score: {overall_score}/100', fill=True, align='C', ln=True)
    pdf.set_font('Helvetica', 'I', 11)
    pdf.cell(0, 8, safe_text(verdict), align='C', ln=True)
    pdf.set_text_color(30, 30, 30)
    pdf.ln(4)

    # ── Category Analysis ─────────────────────────────────────────────────────
    section_colors = {
        'sleep':       (108, 99, 255),
        'stress':      (255, 101, 132),
        'diet':        (0, 191, 166),
        'screen_time': (255, 179, 71),
    }
    section_nums = {'sleep': 3, 'stress': 4, 'diet': 5, 'screen_time': 6}
    labels = {
        'sleep': 'Sleep Analysis',
        'stress': 'Stress Analysis',
        'diet': 'Diet & Nutrition Analysis',
        'screen_time': 'Screen Time Analysis',
    }

    for cat, result in results.items():
        if not result:
            continue
        num = section_nums.get(cat, '')
        label = labels.get(cat, cat.title())
        color = section_colors.get(cat, (100, 100, 100))

        pdf.section_title(f'{num}. {label}', color=color)

        status = result.get('status', 'Unknown')
        score = result.get('score', 0)
        pdf.score_badge(label, score, status)

        # AI Analysis
        analysis = result.get('analysis', '')
        if analysis:
            pdf.set_font('Helvetica', 'B', 10)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(0, 7, 'AI Insight:', ln=True)
            pdf.body_text(analysis[:600])  # Trim very long text

        # Tips / Recommendations
        tips = result.get('tips', [])
        if tips:
            pdf.set_font('Helvetica', 'B', 10)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(0, 7, 'Recommendations:', ln=True)
            rec_texts = [t.get('tip', str(t)) if isinstance(t, dict) else str(t) for t in tips[:5]]
            pdf.bullet_list(rec_texts)

        # Doctor alert
        if result.get('consult_doctor'):
            pdf.set_fill_color(255, 240, 240)
            pdf.set_text_color(200, 50, 50)
            pdf.set_font('Helvetica', 'B', 9)
            pdf.cell(0, 7, '  ! Consider consulting a healthcare professional for this area.', fill=True, ln=True)
            pdf.set_text_color(30, 30, 30)

        pdf.ln(3)

    # ── Daily Routine ─────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_title('7. AI-Generated Daily Routine', color=(72, 61, 139))
    if routine_text:
        pdf.body_text(routine_text[:2000])
    else:
        pdf.body_text('No daily routine was generated. Visit the Daily Routine page to create one.')
    pdf.ln(3)

    # ── AI Suggestions Summary ────────────────────────────────────────────────
    pdf.section_title('8. Key Wellness Suggestions', color=(0, 130, 100))
    suggestions = [
        'Aim for 7-9 hours of quality sleep every night.',
        'Practice 5-10 minutes of deep breathing or meditation daily.',
        'Eat at least 3 balanced meals and drink 8+ glasses of water.',
        'Take a 5-minute break every 45-60 minutes of screen time.',
        'Exercise at least 30 minutes, 3-5 times a week.',
        'Avoid screens 30-60 minutes before bedtime.',
        'Talk to a trusted friend, teacher, or counsellor when feeling overwhelmed.',
        'Maintain a consistent sleep and wake schedule, even on weekends.',
    ]
    pdf.bullet_list(suggestions, color=(40, 40, 40))

    pdf.output(filepath)
    return filepath
