from pymongo import MongoClient

MONGO_URL = "mongodb+srv://grievanceAdmin:yash%407892@cluster0.nbohumo.mongodb.net/grievance_db?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGO_URL)

db = client["grievance_db"]

complaints_collection = db["complaints"]