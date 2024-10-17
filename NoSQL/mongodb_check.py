from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://127.0.0.1:27017')

# Check if MongoDB server is reachable
try:
    client.server_info()
    print("Connected to MongoDB server.")
except Exception as e:
    print(f"Failed to connect to MongoDB server. Error: {e}")
    exit()

# Access the "logs" database and "nginx" collection
logs_db = client.logs
nginx_collection = logs_db.nginx

# Check if the "nginx" collection exists
if "nginx" in logs_db.list_collection_names():
    print("Found 'nginx' collection.")
else:
    print("Error: 'nginx' collection not found.")
    exit()

# Check the number of documents in the "nginx" collection
num_documents = nginx_collection.count_documents({})
print(f"Number of documents in 'nginx' collection: {num_documents}")
