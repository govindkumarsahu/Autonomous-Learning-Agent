import asyncio
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

async def find_all_progress_data():
    mongodb_url = os.getenv("MONGODB_URL")
    client = AsyncIOMotorClient(mongodb_url)
    
    print("🔍 Searching ALL databases for progress data...")
    print("=" * 70)
    
    # Get all databases
    db_names = await client.list_database_names()
    
    total_found = 0
    
    for db_name in db_names:
        db = client[db_name]
        collections = await db.list_collection_names()
        
        # Check for 'progress' collection
        if 'progress' in collections:
            count = await db.progress.count_documents({})
            if count > 0:
                print(f"\n✅ Found data in: {db_name}")
                print(f"   Progress records: {count}")
                
                # Show some records
                cursor = db.progress.find().limit(5)
                records = await cursor.to_list(length=5)
                
                for i, record in enumerate(records, 1):
                    print(f"\n   Record {i}:")
                    print(f"      Topic: {record.get('topic')}")
                    print(f"      Score: {record.get('score')}%")
                    print(f"      Date (MongoDB): {record.get('date')}")
                    print(f"      User ID: {record.get('user_id')}")
                
                total_found += count
    
    print("\n" + "=" * 70)
    print(f"📊 Total progress records found: {total_found}")
    
    if total_found > 0:
        print("\n💡 Data found! I can migrate these timestamps to IST!")
    else:
        print("\n❌ No progress data found in any database")
        print("   Please check MongoDB Compass or Atlas web UI to see where data is stored")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(find_all_progress_data())
