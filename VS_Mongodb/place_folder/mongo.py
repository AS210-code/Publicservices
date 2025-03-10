import pymongo

# Connection string provided by the user
connection_string = "mongodb+srv://ankitasahariamld:NnX60wksmH6mJAcd@cluster0.zzexl.mongodb.net/myDatabase?retryWrites=true&w=majority"


# Create a client connection to MongoDB
client = pymongo.MongoClient(connection_string)

# Access the specific database (myDatabase)
db = client["myDatabase"]

# Choose (or create) a collection for our data
collection = db["sampleCollection"]

# Sample data to insert
sample_data = [
    {"name": "Alice", "age": 30, "city": "New York"},
    {"name": "Bob", "age": 25, "city": "San Francisco"},
    {"name": "Charlie", "age": 35, "city": "Los Angeles"}
]

# Insert the sample data into the collection
insert_result = collection.insert_many(sample_data)
print("Inserted document IDs:", insert_result.inserted_ids)

# ---- Sample Queries ----

# 1. Find one document (e.g., document where name is "Alice")
alice_doc = collection.find_one({"name": "Bob"})
print("\nDocument with name 'Bob':")
print(alice_doc)

# 2. Find all documents where age is greater than 25
print("\nDocuments with age greater than 25:")
for doc in collection.find({"age": {"$gt": 25}}):
    print(doc)

# 3. Count total documents in the collection
doc_count = collection.count_documents({})
print("\nTotal document count in the collection:", doc_count)

# Optional: Clean up by deleting all documents (uncomment if needed)
# collection.delete_many({})