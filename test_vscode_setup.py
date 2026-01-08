"""Diagnostic script to check VS Code setup"""
import os
import sys
from pathlib import Path

print("=" * 60)
print("VS Code Setup Diagnostic")
print("=" * 60)

# Check Python version
print(f"\n1. Python Version: {sys.version}")
print(f"   Python Executable: {sys.executable}")

# Check if running in venv
in_venv = hasattr(sys, 'real_prefix') or (
    hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
)
print(f"\n2. Virtual Environment: {'✓ Active' if in_venv else '✗ Not Active'}")
if in_venv:
    print(f"   Venv Path: {sys.prefix}")

# Check .env file
env_path = Path(__file__).parent / '.env'
print(f"\n3. .env File: {'✓ Found' if env_path.exists() else '✗ Not Found'}")
if env_path.exists():
    print(f"   Path: {env_path.absolute()}")
    # Check file size (don't print contents for security)
    size = env_path.stat().st_size
    print(f"   Size: {size} bytes")

# Check environment variables
print(f"\n4. Environment Variables:")
goog_key = os.getenv("GOOGLE_API_KEY")
gemini_key = os.getenv("GEMINI_API_KEY")
print(f"   GOOGLE_API_KEY: {'✓ Set' if goog_key else '✗ Not Set'}")
print(f"   GEMINI_API_KEY: {'✓ Set' if gemini_key else '✗ Not Set'}")

# Try loading dotenv
try:
    from dotenv import load_dotenv
    print(f"\n5. python-dotenv: ✓ Installed")
    load_dotenv()
    goog_key_after = os.getenv("GOOGLE_API_KEY")
    gemini_key_after = os.getenv("GEMINI_API_KEY")
    print(f"   After load_dotenv():")
    print(f"   GOOGLE_API_KEY: {'✓ Loaded' if goog_key_after else '✗ Not Loaded'}")
    print(f"   GEMINI_API_KEY: {'✓ Loaded' if gemini_key_after else '✗ Not Loaded'}")
except ImportError:
    print(f"\n5. python-dotenv: ✗ Not Installed")
    print("   Run: pip install python-dotenv")

# Check required packages
print(f"\n6. Required Packages:")
packages = ['langchain_google_genai', 'google.genai']
for pkg in packages:
    try:
        __import__(pkg)
        print(f"   {pkg}: ✓ Installed")
    except ImportError:
        print(f"   {pkg}: ✗ Not Installed")

# Test API connection
print(f"\n7. API Connection Test:")
api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if api_key:
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.1
        )
        response = llm.invoke("Say 'Hello' if you can hear me.")
        print(f"   ✓ API Connection Successful!")
        print(f"   Response: {response.content[:50]}...")
    except Exception as e:
        print(f"   ✗ API Connection Failed: {str(e)[:100]}")
else:
    print(f"   ✗ Cannot test - API key not found")

print("\n" + "=" * 60)
print("Diagnostic Complete")
print("=" * 60)

