def classify_complaint(text: str) -> str:
    text = text.lower()

    if any(word in text for word in ["garbage", "waste", "trash", "dustbin", "clean", "sweep", "dump"]):
        return "Sanitation"

    if any(word in text for word in ["pothole", "road", "street", "asphalt", "broken", "pavement"]):
        return "Roads"

    if any(word in text for word in ["water", "leak", "pipe", "drain", "sewage", "flooded", "supply", "plumbing"]):
        return "Water Supply"

    if any(word in text for word in ["streetlight", "electric", "power", "wire", "pole", "shock", "spark", "transformer"]):
        return "Electricity"

    return "General"