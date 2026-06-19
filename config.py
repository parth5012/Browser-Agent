import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not set in environment variables")

# Browser Configuration
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
BROWSER_TIMEOUT = int(os.getenv("BROWSER_TIMEOUT", "30000"))
VIEWPORT_WIDTH = int(os.getenv("VIEWPORT_WIDTH", "1280"))
VIEWPORT_HEIGHT = int(os.getenv("VIEWPORT_HEIGHT", "720"))

# Agent Configuration
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
MAX_ITERATIONS = int(os.getenv("MAX_ITERATIONS", "10"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
