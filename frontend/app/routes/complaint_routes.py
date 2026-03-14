from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.database import complaints_collection
from app.models.complaint_model import Complaint
from app.services.classifier import classify_complaint
from app.services.priority import detect_priority
from app.services.similarity import find_similar_complaints
from app.services.department import assign_department
from app.services.severity import calculate_severity, get_priority_from_score
from app.utils.image_upload import save_image
from datetime import datetime
import random

router = APIRouter()

def generate_complaint_id():
    # Use count + random for a bit more uniqueness but simple format
    count = complaints_collection.count_documents({})
    return f"CMP{1000 + count + random.randint(1, 99)}"

@router.post("/complaints")
async def create_complaint(
    description: str = Form(...),
    location: str = Form(...),
    latitude: float = Form(None),
    longitude: float = Form(None),
    ignore_duplicate: bool = Form(False),
    file: UploadFile = File(None)
):
    try:
        # Check for similarity first if not forced
        if not ignore_duplicate:
            is_duplicate, existing_id = find_similar_complaints(description)
            if is_duplicate:
                return {
                    "duplicate_found": True, 
                    "existing_complaint_id": existing_id,
                    "message": f"A similar complaint already exists with ID: {existing_id}"
                }

        category = classify_complaint(description)
        severity_score = calculate_severity(description)
        priority = get_priority_from_score(severity_score)
        department = assign_department(category)
        complaint_id = generate_complaint_id()

        image_filename = None
        if file:
            image_filename = save_image(file)

        data = {
            "id": complaint_id,
            "description": description,
            "location": location,
            "latitude": latitude,
            "longitude": longitude,
            "category": category,
            "priority": priority,
            "severity_score": severity_score,
            "department": department,
            "status": "Pending",
            "image": image_filename,
            "created_at": datetime.now().isoformat()
        }

        if severity_score >= 8:
            data["emergency"] = True

        complaints_collection.insert_one(data)

        # Make sure we don't return the _id ObjectId from MongoDB
        return {
            "complaint_id": complaint_id, 
            "status": "Pending", 
            "message": "Complaint submitted successfully",
            "emergency": severity_score >= 8
        }
    except Exception as e:
        import logging
        logging.error(f"Error creating complaint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to submit complaint: {str(e)}")


@router.get("/complaints")
def get_complaints():
    try:
        complaints = list(complaints_collection.find({}, {"_id": 0}))
        # Sort by recent first purely for convenience
        complaints.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return complaints
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching complaints: {str(e)}")


@router.get("/complaints/{id}")
def get_complaint(id: str):
    try:
        complaint = complaints_collection.find_one({"id": id}, {"_id": 0})
        if not complaint:
            raise HTTPException(status_code=404, detail="Complaint not found")
        return complaint
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching complaint: {str(e)}")


@router.put("/complaints/{id}/status")
def update_status(id: str, status: str):
    valid_statuses = ["Pending", "In Progress", "Resolved", "Rejected"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of {valid_statuses}")
        
    try:
        result = complaints_collection.update_one(
            {"id": id},
            {"$set": {"status": status}}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Complaint not found")
            
        return {"message": "Status updated successfully", "status": status}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating status: {str(e)}")