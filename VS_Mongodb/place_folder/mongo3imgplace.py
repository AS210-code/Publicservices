import os
import pymongo

# MongoDB connection string provided by the user
connection_string = "mongodb+srv://ankitasahariamld:NnX60wksmH6mJAcd@cluster0.zzexl.mongodb.net/Services?retryWrites=true&w=majority"
client = pymongo.MongoClient(connection_string)

# Access the specific database and collection
db = client["Services"]
images_collection = db["images"]

# The filename of the image to fetch from the database
image_filename = "image.png"

# Fetch the image document from MongoDB by its filename
image_doc = images_collection.find_one({"filename": image_filename})

if not image_doc:
    print(f"No image found in the database with filename: {image_filename}")
else:
    # Folder at the root where the image will be saved
    folder_name = "place_folder"
    
    # Create the folder if it does not exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    # Path to save the image
    file_path = os.path.join(folder_name, image_filename)
    
    # Write the binary data to the file
    with open(file_path, "wb") as file:
        file.write(image_doc["data"])
    
    print(f"Image '{image_filename}' fetched from MongoDB and saved to '{file_path}'.")
