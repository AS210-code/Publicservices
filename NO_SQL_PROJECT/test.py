from pymongo import MongoClient

# Connect to your MongoDB cluster
client = MongoClient("your_cluster_key")

# Choose the database
db = client["myDatabase"]

# Create a collection (or get it if it already exists)
collection = db["testCollection"]

# Sample data to insert
data = {
    "name": "Maya",
    "project": "MongoDB test insert",
    "skills": ["Python", "MongoDB", "Cloud", "AI"],
    "status": "active"
}

# Insert the data
inserted = collection.insert_one(data)

# Confirm insertion
print(f"Data inserted with ID: {inserted.inserted_id}")

