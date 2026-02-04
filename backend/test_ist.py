import pytz
from datetime import datetime

# Test IST timezone
ist = pytz.timezone('Asia/Kolkata')
current_time_ist = datetime.now(ist)

print(f"✅ Current IST time: {current_time_ist}")
print(f"✅ Formatted: {current_time_ist.strftime('%d %b %Y, %I:%M:%S %p')}")
print(f"✅ This should match your system time!")
