import asyncio
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

async def check_all_databases():
    mongodb_url = os.getenv("MONGODB_URL")
    print(f"🔗 Connecting to: {mongodb_url[:50]}...")
    print()
    
    client = AsyncIOMotorClient(mongodb_url)
    
    # List all databases
    db_names = await client.list_database_names()
    print(f"📚 Available databases: {db_names}")
    print()
    
    # Check each database for progress collections
    for db_name in db_names:
        if db_name in ['admin', 'local', 'config']:
            continue
        
        db = client[db_name]
        collections = await db.list_collection_names()
        
        if 'progress' in collections:
            count = await db.progress.count_documents({})
            print(f"✅ Database: {db_name}")
            print(f"   Collections: {collections}")
            print(f"   Progress records: {count}")
            
            if count > 0:
                # Show latest record
                latest = await db.progress.find_one(sort=[("date", -1)])
                print(f"   Latest record:")
                print(f"      Topic: {latest['topic']}")
                print(f"      Score: {latest['score']}%")
                print(f"      Date: {latest['date']}")
            print()
    
    # Check our specific database
    db = client["autonomous_learning_agent"]
    collections = await db.list_collection_names()
    progress_count = await db.progress.count_documents({})
    users_count = await db.users.count_documents({})
    
    print("🎯 Target Database: autonomous_learning_agent")
    print(f"   Collections: {collections}")
    print(f"   Users: {users_count}")
    print(f"   Progress records: {progress_count}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check_all_databases())
