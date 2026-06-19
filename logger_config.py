from loguru import logger
import sys
from config import LOG_LEVEL

# Configure logger
logger.remove()
logger.add(
    sys.stdout,
    format="<level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level=LOG_LEVEL,
)

logger.add(
    "logs/browser_agent.log",
    rotation="500 MB",
    retention="10 days",
    level=LOG_LEVEL,
)

__all__ = ["logger"]
