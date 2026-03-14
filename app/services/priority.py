def detect_priority(text):

    text = text.lower()

    high_keywords = ["flood", "accident", "traffic jam", "vehicles stuck", "emergency"]
    medium_keywords = ["pothole", "garbage", "road damage", "water leakage"]
    low_keywords = ["flicker", "dim light"]

    if any(word in text for word in high_keywords):
        return "High"

    if any(word in text for word in medium_keywords):
        return "Medium"

    if any(word in text for word in low_keywords):
        return "Low"

    return "Medium"