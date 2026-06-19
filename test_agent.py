#!/usr/bin/env python3
"""
Quick test of the Browser Agent
"""
import os
import asyncio
from dotenv import load_dotenv

# Load environment
load_dotenv()

print("\n" + "="*70)
print("  BROWSER AGENT - QUICK TEST")
print("="*70 + "\n")

# Check requirements
print("Checking installation status...\n")

checks = {
    "langchain": False,
    "langgraph": False,
    "groq": False,
    "playwright": False,
    "loguru": False,
}

for package in checks:
    try:
        __import__(package.replace("_", "-"))
        checks[package] = True
        print(f"✓ {package:20} - Installed")
    except ImportError:
        print(f"✗ {package:20} - Missing")

print("\n" + "="*70)

# Check API key
api_key = os.getenv("GROQ_API_KEY", "").strip()
if api_key and api_key != "your_groq_api_key_here":
    print(f"✓ Groq API Key     - Configured (key found)")
else:
    print(f"✗ Groq API Key     - NOT configured")
    print(f"\n  To use this agent, you need to:")
    print(f"  1. Get a free API key: https://console.groq.com")
    print(f"  2. Edit .env file and add your key:")
    print(f"     GROQ_API_KEY=your_actual_key_here")
    print(f"\n")

print("="*70)

# Try importing agent
print("\nTrying to import Browser Agent...\n")
try:
    from browser_agent import BrowserAgent
    from logger_config import logger
    print("✓ Successfully imported BrowserAgent!")
    print("✓ Successfully imported Logger!")
    
    print("\n" + "="*70)
    print("  AGENT COMPONENTS LOADED")
    print("="*70 + "\n")
    
    print("Available agent methods:")
    print("  • execute_task(task_description)")
    print("  • interactive_session()")
    
    print("\nAvailable CLI commands:")
    print("  • python main.py interactive  - Interactive mode")
    print("  • python main.py task 'desc'  - Single task")
    print("  • python main.py batch file   - Batch processing")
    print("  • python main.py config       - Show configuration")
    
    print("\n" + "="*70)
    
    if api_key and api_key != "your_groq_api_key_here":
        print("\n✓ Ready to run! Starting interactive session...\n")
        print("="*70 + "\n")
        
        async def run():
            agent = BrowserAgent()
            await agent.interactive_session()
        
        asyncio.run(run())
    else:
        print("\n⚠ Cannot run agent - Groq API key not configured")
        print("\nTo test, you can:")
        print("1. Add your API key to .env: GROQ_API_KEY=your_key_here")
        print("2. Run: python test_agent.py")
        print("\nOr run in interactive CLI mode:")
        print("python main.py interactive")
        
except ImportError as e:
    print(f"✗ Failed to import agent: {e}")
    print(f"\nPlease run: pip install -r requirements.txt")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
