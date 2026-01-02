def validate_register(data):
    if not data:
        return {"error": True,"message": "Data is required"}
    if not data.get("email"):
        return {"error": True,"message": "Email is required"}
    if not data.get("password"):
        return {"error": True,"message": "Password is required"}
    if not data.get("name"):
        return {"error": True,"message": "Name is required"}
    return {"error": False,"message": "User registered successfully"}