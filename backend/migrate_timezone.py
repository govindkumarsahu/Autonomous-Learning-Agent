"""
MongoDB Time Migration Script
This script converts all existing UTC timestamps in the database to IST (Indian Standard Time)
"""
import asyncio
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
import pytz

load_dotenv()

async def migrate_timestamps_to_ist():
    mongodb_url = os.getenv("MONGODB_URL")
    client = AsyncIOMotorClient(mongodb_url)
    db = client["autonomous_learning_agent"]
    
    ist = pytz.timezone('Asia/Kolkata')
    utc = pytz.UTC
    
    print("🔄 Starting timestamp migration to IST...")
    print("=" * 60)
    
    # Migrate progress collection
    progress_records = await db.progress.find().to_list(length=1000)
    
    if not progress_records:
        print("❌ No progress records found in database")
        return
    
    print(f"📊 Found {len(progress_records)} progress records")
    print()
    
    updated_count = 0
    for record in progress_records:
        old_date = record['date']
        
        # Convert to IST
        if isinstance(old_date, datetime):
            # If naive datetime, treat as UTC
            if old_date.tzinfo is None:
                utc_date = utc.localize(old_date)
            else:
                utc_date = old_date
            
            # Convert to IST (add 5:30 hours)
            ist_date = utc_date.astimezone(ist)
            
            # Update in database
            await db.progress.update_one(
                {"_id": record["_id"]},
                {"$set": {"date": ist_date}}
            )
            
            print(f"✅ Updated record for topic '{record['topic']}'")
            print(f"   Old (UTC):  {old_date}")
            print(f"   New (IST):  {ist_date}")
            print(f"   Display:    {ist_date.strftime('%d %b %Y, %I:%M:%S %p')}")
            print()
            
            updated_count += 1
    
    # Migrate users collection
    users = await db.users.find().to_list(length=1000)
    for user in users:
        if 'created_at' in user:
            old_date = user['created_at']
            
            if isinstance(old_date, datetime):
                if old_date.tzinfo is None:
                    utc_date = utc.localize(old_date)
                else:
                    utc_date = old_date
                
                ist_date = utc_date.astimezone(ist)
                
                await db.users.update_one(
                    {"_id": user["_id"]},
                    {"$set": {"created_at": ist_date}}
                )
    
    print("=" * 60)
    print(f"✅ Migration complete!")
    print(f"📊 Updated {updated_count} progress records")
    print(f"📊 Updated {len(users)} user records")
    print()
    print("🎉 All timestamps are now in IST (Asia/Kolkata)")
    print("💡 Refresh your browser to see the updated times!")
    
    client.close()

if __name__ == "__main__":
    print()
    print("╔════════════════════════════════════════════════════════════╗")
    print("║     MongoDB Timestamp Migration Tool - UTC to IST         ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    asyncio.run(migrate_timestamps_to_ist())
