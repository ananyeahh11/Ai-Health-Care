import json
import os

USER_DATA_FILE = "data/user_data.json"

def load_user_history():
    """Load historical scores to show trends."""
    if not os.path.exists(USER_DATA_FILE):
        return []
    
    try:
        with open(USER_DATA_FILE, "r") as f:
            data = json.load(f)
            return data.get("history", [])
    except Exception:
        return []

def save_assessment_to_history(user_profile, results):
    """Save a snapshot of the current assessment to history."""
    if not os.path.exists(USER_DATA_FILE):
        data = {"profiles": [], "history": []}
    else:
        try:
            with open(USER_DATA_FILE, "r") as f:
                data = json.load(f)
        except Exception:
            data = {"profiles": [], "history": []}
            
    # Compile snapshot
    from datetime import datetime
    snapshot = {
        "timestamp": datetime.now().isoformat(),
        "user_name": user_profile.get("name", "Student"),
        "scores": {}
    }
    
    for cat, res in results.items():
        if res:
            snapshot["scores"][cat] = res.get("score", 0)
            
    if not snapshot["scores"]:
        return False
        
    data["history"].append(snapshot)
    
    with open(USER_DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
        
    return True
