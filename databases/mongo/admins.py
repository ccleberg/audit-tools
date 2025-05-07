from pymongo import MongoClient

# Connect to the MongoDB server
client = MongoClient("mongodb://localhost:27017/")

# Select the 'admin' database
db = client.admin

# Query the 'system.users' collection
users = db.system.users.find(
    {}, {"user": 1, "db": 1, "roles": 1, "credentials": 1, "userSource": 1}
)

# Print the results in a pretty format
for user in users:
    print(user)
