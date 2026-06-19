#!/usr/bin/env python3
"""
Quick start guide and setup utility for the browser agent.
Run this to verify installation and configure the agent.
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Tuple

def print_header(text: str):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def print_step(step_num: int, text: str):
    """Print a numbered step."""
    print(f"  [{step_num}] {text}")


def check_python_version() -> bool:
    """Check Python version."""
    print_step(1, "Checking Python version...")
    
    required_version = (3, 10)
    current_version = sys.version_info[:2]
    
    if current_version >= required_version:
        print(f"  ✓ Python {current_version[0]}.{current_version[1]} (Required: {required_version[0]}.{required_version[1]}+)")
        return True
    else:
        print(f"  ✗ Python {current_version[0]}.{current_version[1]} is too old")
        print(f"  Please install Python {required_version[0]}.{required_version[1]} or later")
        return False


def check_dependencies() -> bool:
    """Check if required packages are installed."""
    print_step(2, "Checking dependencies...")
    
    required_packages = [
        "langchain",
        "langgraph",
        "langchain_community",
        "langchain_groq",
        "playwright",
        "dotenv",
        "pydantic",
        "loguru",
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("_", "-").split("[")[0])
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} (missing)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n  Missing packages: {', '.join(missing_packages)}")
        print(f"  Run: pip install -r requirements.txt")
        return False
    
    return True


def check_playwright_browsers() -> bool:
    """Check if Playwright browsers are installed."""
    print_step(3, "Checking Playwright browsers...")
    
    try:
        from playwright.sync_api import sync_playwright
        
        # Quick check
        print("  ✓ Playwright is installed")
        print("  Note: Run 'playwright install' to download browsers if needed")
        return True
    except ImportError:
        print("  ✗ Playwright is not installed")
        return False


def check_env_file() -> bool:
    """Check if .env file exists and has API key."""
    print_step(4, "Checking environment configuration...")
    
    env_file = Path(".env")
    
    if not env_file.exists():
        print("  ✗ .env file not found")
        print("  Copy .env.example to .env and add your Groq API key")
        return False
    
    with open(env_file) as f:
        content = f.read()
    
    if "GROQ_API_KEY=" in content:
        if "your_groq_api_key_here" in content or "GROQ_API_KEY=" in content and "GROQ_API_KEY=" == content.split("\n")[0].split("=")[0] + "=":
            print("  ⚠ .env exists but GROQ_API_KEY is not set")
            print("  Get your API key from: https://console.groq.com")
            return False
        else:
            print("  ✓ .env file configured")
            return True
    else:
        print("  ⚠ GROQ_API_KEY not found in .env")
        return False


def install_dependencies() -> bool:
    """Install required dependencies."""
    print_step(5, "Installing dependencies...")
    
    try:
        print("  Running: pip install -r requirements.txt")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            check=True,
            capture_output=True
        )
        print("  ✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Failed to install dependencies")
        print(f"  Error: {e}")
        return False


def install_playwright_browsers() -> bool:
    """Install Playwright browsers."""
    print_step(6, "Installing Playwright browsers...")
    
    try:
        print("  Running: playwright install")
        subprocess.run(
            ["playwright", "install"],
            check=True,
            capture_output=True
        )
        print("  ✓ Playwright browsers installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"  ✗ Failed to install Playwright browsers")
        print(f"  Run manually: playwright install")
        return False


def setup_env_file() -> bool:
    """Set up .env file if it doesn't exist."""
    env_file = Path(".env")
    
    if env_file.exists():
        return True
    
    print("\n" + "=" * 60)
    print("  Setting up .env file...")
    print("=" * 60 + "\n")
    
    env_content = """# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here

# Browser Settings
HEADLESS=false
BROWSER_TIMEOUT=30000
VIEWPORT_WIDTH=1280
VIEWPORT_HEIGHT=720

# Agent Settings
MODEL_NAME=llama-3.3-70b-versatile
MAX_ITERATIONS=10
TEMPERATURE=0.7

# Logging
LOG_LEVEL=INFO
"""
    
    try:
        with open(env_file, "w") as f:
            f.write(env_content)
        print("  ✓ .env file created")
        print("  ⚠ Please edit .env and add your Groq API key")
        return False  # Return False because API key still needs to be set
    except Exception as e:
        print(f"  ✗ Failed to create .env file: {e}")
        return False


def run_setup(auto: bool = False) -> bool:
    """Run the complete setup."""
    print_header("Browser Agent - Setup & Verification")
    
    checks = [
        ("Python Version", check_python_version),
        ("Environment File", setup_env_file),
        ("Dependencies", check_dependencies if not auto else None),
        ("Playwright Browsers", check_playwright_browsers),
        ("Environment Configuration", check_env_file),
    ]
    
    all_passed = True
    
    for check_name, check_func in checks:
        if check_func is None:
            continue
        
        try:
            if not check_func():
                all_passed = False
        except Exception as e:
            print(f"  ✗ Error: {e}")
            all_passed = False
    
    return all_passed


def show_next_steps():
    """Show next steps for the user."""
    print_header("Next Steps")
    
    print("""
  1. Edit .env file and add your Groq API key:
     - Get free API key at: https://console.groq.com
     - Copy your API key and paste it in .env
  
  2. Ensure Playwright browsers are installed:
     $ playwright install
  
  3. Run example tasks:
     $ python examples.py
  
  4. Or execute a simple task:
     $ python -c "
       import asyncio
       from browser_agent import BrowserAgent
       
       async def main():
           agent = BrowserAgent()
           result = await agent.execute_task('Go to google.com')
           print(result)
       
       asyncio.run(main())
       "
  
  5. Try interactive mode:
     $ python examples.py
     Select option: 3
  
  6. Read the documentation:
     Check README.md for detailed usage examples
    """)


def main():
    """Main setup entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Browser Agent Setup")
    parser.add_argument("--auto", action="store_true", help="Auto-install dependencies")
    parser.add_argument("--install", action="store_true", help="Install all dependencies")
    
    args = parser.parse_args()
    
    if args.install:
        print_header("Installing Dependencies")
        install_dependencies()
        install_playwright_browsers()
        return
    
    # Run verification
    all_passed = run_setup(auto=args.auto)
    
    # Show results
    print_header("Setup Results")
    
    if all_passed:
        print("  ✓ All checks passed! You're ready to go.\n")
    else:
        print("  ⚠ Some checks failed. See above for details.\n")
    
    show_next_steps()


if __name__ == "__main__":
    main()
