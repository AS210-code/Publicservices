import os
import pymongo
from bson.binary import Binary

# Connection string provided by the user
connection_string = "mongodb+srv://ankitasahariamld:NnX60wksmH6mJAcd@cluster0.zzexl.mongodb.net/Services?retryWrites=true&w=majority"

# Create a client connection to MongoDB
client = pymongo.MongoClient(connection_string)

# Access the specific database (myDatabase)
db = client["Services"]

# --- Inserting Sample Data into 'sampleCollection' ---

# Choose (or create) a collection for sample data
sample_collection = db["sampleServices"]

# Sample data to insert
sample_data = [
    {"name": "Alice", "age": 30, "city": "New York"},
    {"name": "Bob", "age": 25, "city": "San Francisco"},
    {"name": "Charlie", "age": 35, "city": "Los Angeles"}
]

# Insert the sample data into the collection
insert_result = sample_collection.insert_many(sample_data)
print("Inserted document IDs for sample data:", insert_result.inserted_ids)

# ---- Sample Queries ----

# 1. Find one document (e.g., document where name is "Alice")
alice_doc = sample_collection.find_one({"name": "Alice"})
print("\nDocument with name 'Alice':")
print(alice_doc)

# 2. Find all documents where age is greater than 25
print("\nDocuments with age greater than 25:")
for doc in sample_collection.find({"age": {"$gt": 25}}):
    print(doc)

# 3. Count total documents in the collection
doc_count = sample_collection.count_documents({})
print("\nTotal document count in the collection:", doc_count)

# --- Inserting Images from the 'dataset' Folder into a Separate Collection ---

# Create (or use) a collection for images
images_collection = db["images"]

# Path to the dataset folder containing images (adjust the folder name if needed)
dataset_folder = "dataset"

if not os.path.exists(dataset_folder):
    print(f"Directory '{dataset_folder}' does not exist.")
else:
    # Iterate through each file in the dataset folder
    for filename in os.listdir(dataset_folder):
        # Filter files by common image extensions (adjust as necessary)
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            file_path = os.path.join(dataset_folder, filename)
            with open(file_path, "rb") as image_file:
                image_data = image_file.read()

            # Create a document with the binary image data
            image_document = {
                "filename": filename,
                "data": Binary(image_data)
            }

            result = images_collection.insert_one(image_document)
            print(f"Inserted image '{filename}' with ID: {result.inserted_id}")