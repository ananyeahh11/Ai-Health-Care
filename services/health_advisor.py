"""
Health Advisor — provides wellness assessments and personalized tips.
"""

import json
from utils.helper import load_json, get_score_status, save_report, generate_report_filename
from utils.constants import DISCLAIMER_SHORT
from services.score_calculator import (calculate_sleep_score, calculate_stress_score,
                                       calculate_diet_score, calculate_screen_time_score)



class HealthAdvisor:
    """Analyzes assessment data and provides wellness recommendations."""

    def __init__(self, llm_service):
        """
        Initialize with LLM service and load data files.

        Args:
            llm_service: An instance of LLMService.
        """
        self.llm = llm_service
        self.wellness_tips = load_json("data/wellness_tips.json")
        self.health_guidelines = load_json("data/health_guidelines.json")

    def assess_sleep(self, answers: dict) -> dict:
        """
        Analyze sleep assessment data and return results.

        Args:
            answers: Dictionary of sleep questionnaire responses.

        Returns:
            Dict with score, status, analysis text, tips, and consult_doctor flag.
        """
        # Calculate base score
        score = calculate_sleep_score(answers)
        status_info = get_score_status(score)

        # Get AI analysis
        guidelines_context = json.dumps(self.health_guidelines.get("sleep", {}), indent=2)
        analysis_input = answers.copy()
        analysis_input["calculated_score"] = score
        analysis_input["status"] = status_info["label"]

        ai_analysis = self.llm.generate_assessment_response(
           "sleep",
            analysis_input,
            guidelines_context
            )

        # Get relevant tips
        tips = self._get_tips("sleep", score)

        # Check if doctor consultation needed
        consult_doctor = score < 40 or answers.get("hours", 7) < 5

        return {
            "score": score,
            "status": status_info["label"],
            "status_color": status_info["color"],
            "status_emoji": status_info["emoji"],
            "analysis": ai_analysis,
            "tips": tips,
            "consult_doctor": consult_doctor,
            "consult_reasons": self.health_guidelines.get("sleep", {}).get("consult_doctor_when", [])
        }

    def assess_stress(self, answers: dict) -> dict:
        """
        Analyze stress assessment data and return results.

        Args:
            answers: Dictionary of stress questionnaire responses.

        Returns:
            Dict with score, status, analysis text, tips, and consult_doctor flag.
        """
        score = calculate_stress_score(answers)
        status_info = get_score_status(score)

        guidelines_context = json.dumps(self.health_guidelines.get("stress", {}), indent=2)
        analysis_input = answers.copy()
        analysis_input["calculated_score"] = score
        analysis_input["status"] = status_info["label"]

        ai_analysis = self.llm.generate_assessment_response(
            "stress",
            analysis_input,
            guidelines_context
)

        tips = self._get_tips("stress", score)
        consult_doctor = score < 40 or answers.get("level", 5) >= 8

        return {
            "score": score,
            "status": status_info["label"],
            "status_color": status_info["color"],
            "status_emoji": status_info["emoji"],
            "analysis": ai_analysis,
            "tips": tips,
            "consult_doctor": consult_doctor,
            "consult_reasons": self.health_guidelines.get("stress", {}).get("consult_doctor_when", [])
        }

    def assess_diet(self, answers: dict) -> dict:
        """
        Analyze diet assessment data and return results.

        Args:
            answers: Dictionary of diet questionnaire responses.

        Returns:
            Dict with score, status, analysis text, tips, and consult_doctor flag.
        """
        score = calculate_diet_score(answers)
        status_info = get_score_status(score)

        guidelines_context = json.dumps(self.health_guidelines.get("diet", {}), indent=2)
        analysis_input = answers.copy()
        analysis_input["calculated_score"] = score
        analysis_input["status"] = status_info["label"]

        ai_analysis = self.llm.generate_assessment_response(
            "diet",
            analysis_input,
            guidelines_context
)

        tips = self._get_tips("diet", score)
        consult_doctor = score < 30

        return {
            "score": score,
            "status": status_info["label"],
            "status_color": status_info["color"],
            "status_emoji": status_info["emoji"],
            "analysis": ai_analysis,
            "tips": tips,
            "consult_doctor": consult_doctor,
            "consult_reasons": self.health_guidelines.get("diet", {}).get("consult_doctor_when", [])
        }

    def assess_screen_time(self, answers: dict) -> dict:
        """
        Analyze screen time assessment data and return results.

        Args:
            answers: Dictionary of screen time questionnaire responses.

        Returns:
            Dict with score, status, analysis text, tips, and consult_doctor flag.
        """
        score = calculate_screen_time_score(answers)
        status_info = get_score_status(score)

        guidelines_context = json.dumps(self.health_guidelines.get("screen_time", {}), indent=2)
        analysis_input = answers.copy()
        analysis_input["calculated_score"] = score
        analysis_input["status"] = status_info["label"]

        ai_analysis = self.llm.generate_assessment_response(
            "screen time",
            analysis_input,
            guidelines_context
)

        tips = self._get_tips("screen_time", score)
        consult_doctor = answers.get("eye_strain", False) and answers.get("daily_hours", 0) > 10

        return {
            "score": score,
            "status": status_info["label"],
            "status_color": status_info["color"],
            "status_emoji": status_info["emoji"],
            "analysis": ai_analysis,
            "tips": tips,
            "consult_doctor": consult_doctor,
            "consult_reasons": self.health_guidelines.get("screen_time", {}).get("consult_doctor_when", [])
        }

    def generate_report(self, user_name: str, user_age: int, student_type: str,
                        assessment_results: dict) -> dict:
        """
        Generate a comprehensive wellness report from all assessments.

        Args:
            user_name: The user's name.
            user_age: The user's age.
            student_type: Type of student.
            assessment_results: Dict with category keys and assessment result values.

        Returns:
            Dict with overall_score, category_scores, and report markdown.
        """
        from models.wellness_report import WellnessReport, CategoryScore
        from utils.helper import format_timestamp
        from utils.pdf_generator import generate_pdf_report

        category_scores = []
        total_score = 0
        count = 0

        for category, result in assessment_results.items():
            if result:
                cat_score = {
                    "category": category,
                    "score": result.get("score", 0),
                    "status": result.get("status", "unknown").lower().replace(" ", "_"),
                    "key_findings": [],
                    "recommendations": [tip["tip"] for tip in result.get("tips", [])[:3]]
                }
                category_scores.append(cat_score)
                total_score += result.get("score", 0)
                count += 1

        overall_score = round(total_score / count, 1) if count > 0 else 0

        report = WellnessReport(
            user_name=user_name,
            user_age=user_age,
            student_type=student_type,
            overall_score=overall_score,
            category_scores=category_scores,
        )

        # Generate PDF report
        filename = generate_report_filename(user_name).replace('.md', '.pdf')
        filepath = f"reports/generated_reports/{filename}"
        
        generate_pdf_report(
            user_name, user_age, student_type, overall_score, category_scores, filepath
        )

        return {
            "overall_score": overall_score,
            "category_scores": category_scores,
            "report_markdown": report.to_markdown(),
            "filepath": filepath
        }

    # ──────────────────────── Report Generators ────────────────────────


    def _get_tips(self, category: str, score: float) -> list:
        """Get relevant wellness tips based on category and score."""
        all_tips = self.wellness_tips.get(category, [])

        if score < 40:
            return [t for t in all_tips if t.get("priority") == "high"][:5]
        elif score < 70:
            return [t for t in all_tips if t.get("priority") in ("high", "medium")][:4]
        else:
            return all_tips[:3]
