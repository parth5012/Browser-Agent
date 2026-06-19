#!/usr/bin/env python3
"""Browser Agent Demo"""
import os
import sys
import asyncio
from dotenv import load_dotenv

load_dotenv()

print("\n" + "="*70)
print("  BROWSER AGENT - COMPONENT CHECK")
print("="*70 + "\n")

# Check requirements
packages = ["langchain", "langgraph", "groq", "playwright", "loguru"]
missing = []

for pkg in packages:
    try:
        __import__(pkg)
        print("[+] {} installed".format(pkg))
    except ImportError:
        missing.append(pkg)
        print("[-] {} missing".format(pkg))

print("\n" + "="*70)

api_key = os.getenv("GROQ_API_KEY", "").strip()
if api_key and api_key != "your_groq_api_key_here":
    print("[+] Groq API Key: Configured")
else:
    print("[-] Groq API Key: NOT configured")

print("\n" + "="*70 + "\n")

if missing:
    print("Missing packages - cannot run agent")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)

if not api_key or api_key == "your_groq_api_key_here":
    print("Groq API key not configured!")
    print("\nTo run the agent:")
    print("1. Get a free API key: https://console.groq.com")
    print("2. Edit .env and add: GROQ_API_KEY=your_key_here")
    print("3. Run: python main.py interactive")
    sys.exit(0)

print("\nAll components ready! Starting agent...\n")
print("="*70 + "\n")

try:
    from browser_agent import BrowserAgent
    from logger_config import logger
    
    async def main():
        agent = BrowserAgent()
        await agent.interactive_session()
    
    asyncio.run(main())

except Exception as e:
    print("Error: {}".format(e))
    import traceback
    traceback.print_exc()
