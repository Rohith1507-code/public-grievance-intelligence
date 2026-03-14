def calculate_severity(text: str) -> int:
    """
    Calculates a severity score based on keywords in the complaint description.
    """
    text = text.lower()
    score = 0
    
    # Severity keyword mapping
    weights = {
        "flood": 4,
        "accident": 4,
        "fire": 5,
        "vehicles stuck": 3,
        "stuck": 2,
        "pothole": 2,
        "garbage": 2,
        "streetlight": 1,
        "electric": 3,
        "shock": 4,
        "spark": 4,
        "explosion": 5,
        "emergency": 3,
        "urgent": 2,
        "danger": 3,
        "broken": 1,
        "leak": 2,
        "sewage": 2,
        "drain": 2
    }
    
    for word, weight in weights.items():
        if word in text:
            score += weight
            
    return score

def get_priority_from_score(score: int) -> str:
    """
    Maps a severity score to a priority level.
    """
    if score >= 8:
        return "High"
    elif score >= 4:
        return "Medium"
    else:
        return "Low"
