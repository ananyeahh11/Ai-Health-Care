def calculate_overall_metrics(results):
    """Calculates top level KPIs from assessment results."""
    completed = 0
    total_score = 0
    categories = ["sleep", "stress", "diet", "screen_time"]
    
    for cat in categories:
        if results.get(cat):
            completed += 1
            total_score += results[cat].get("score", 0)
            
    average = round(total_score / completed, 1) if completed > 0 else 0
    
    return {
        "completed_count": completed,
        "total_categories": 4,
        "average_score": average,
        "progress_percent": (completed / 4) * 100
    }
