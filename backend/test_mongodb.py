import asyncio
import sys
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

async def test_mongodb():
    try:
        mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        print(f"📡 Testing connection to: {mongodb_url[:50]}...")
        
        # Try to connect
        client = AsyncIOMotorClient(mongodb_url, serverSelectionTimeoutMS=5000)
        
        # Test the connection
        await client.admin.command('ping')
        
        print("✅ MongoDB connection successful!")
        print(f"   Server info: {await client.server_info()}")
        
        # List databases
        db_list = await client.list_database_names()
        print(f"   Available databases: {db_list}")
        
        return True
        
    except Exception as e:
        print("❌ MongoDB connection failed!")
        print(f"   Error: {str(e)}")
        print("\n💡 Solutions:")
        print("   1. Start local MongoDB: mongod --dbpath C:\\data\\db")
        print("   2. Or use MongoDB Atlas (cloud) - see MONGODB_SETUP.md")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_mongodb())
    sys.exit(0 if result else 1)
