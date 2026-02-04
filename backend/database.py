import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = "autonomous_learning_agent"

client = AsyncIOMotorClient(MONGODB_URL)
database = client[DATABASE_NAME]


def get_database():
    return database
