from difflib import SequenceMatcher
from app.database import complaints_collection

def find_similar_complaints(description, threshold=0.7):
    """
    Finds if any existing complaint has a similar description.
    Returns a tuple (is_duplicate, existing_complaint_id)
    """
    # Fetch all existing complaints' descriptions and IDs
    # In a large-scale system, we'd use vector search or indexing,
    # but for a hackathon, iterating through recent complaints is fine.
    existing_complaints = list(complaints_collection.find({}, {"description": 1, "id": 1}))
    
    for complaint in existing_complaints:
        existing_desc = complaint.get("description", "")
        # Calculate similarity ratio using difflib (0.0 to 1.0)
        similarity = SequenceMatcher(None, description.lower(), existing_desc.lower()).ratio()
        
        if similarity >= threshold:
            return True, complaint.get("id")
            
    return False, None
