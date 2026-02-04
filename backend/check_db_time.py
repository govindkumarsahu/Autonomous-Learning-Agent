import asyncio
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import pytz

load_dotenv()

async def check_latest_progress():
    mongodb_url = os.getenv("MONGODB_URL")
    client = AsyncIOMotorClient(mongodb_url)
    db = client["autonomous_learning_agent"]
    
    # Get the latest progress record
    latest = await db.progress.find_one(sort=[("date", -1)])
    
    if latest:
        print("📊 Latest Progress Record:")
        print(f"   Topic: {latest['topic']}")
        print(f"   Score: {latest['score']}%")
        print(f"   Date (raw from DB): {latest['date']}")
        print(f"   Date type: {type(latest['date'])}")
        
        # Check if it has timezone info
        if hasattr(latest['date'], 'tzinfo'):
            print(f"   Timezone info: {latest['date'].tzinfo}")
        
        # Convert to IST for display
        ist = pytz.timezone('Asia/Kolkata')
        if isinstance(latest['date'], datetime):
            if latest['date'].tzinfo is None:
                # Naive datetime - assume UTC
                utc_date = latest['date'].replace(tzinfo=pytz.UTC)
                ist_date = utc_date.astimezone(ist)
                print(f"   ⚠️  Naive datetime detected (no timezone)")
                print(f"   Converted to IST: {ist_date}")
            else:
                print(f"   ✅ Timezone-aware datetime")
                print(f"   In IST: {latest['date'].astimezone(ist)}")
    else:
        print("❌ No progress records found")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check_latest_progress())
