from logger import Logger
from pymongo.database import Database
from pymongo.mongo_client import MongoClient
# docker run -d --name tab_cleaner_mongodb -p 27019:27017 mongo
uri = "mongodb://localhost:27019"
Logger.log(f"Creating Mongo client at {uri}...")
client = MongoClient(uri)

try:
    client.admin.command("ping")
    Logger.log("Connected to Mongo server (db.py)")
except Exception as e:
    Logger.log(f"Exception connecting to Mongo server: {e}")

db: Database = client.get_database("data")
