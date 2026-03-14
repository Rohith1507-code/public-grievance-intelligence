def assign_department(category: str) -> str:
    """
    Automatically assigns a government department based on the complaint category.
    """
    mapping = {
        "Sanitation": "Municipal Sanitation Department",
        "Roads": "Road Infrastructure Department",
        "Water Supply": "Water Board",
        "Electricity": "Electricity Board",
        "General": "City Administration"
    }
    
    # Return the mapped department or "City Administration" as a default
    return mapping.get(category, "City Administration")
