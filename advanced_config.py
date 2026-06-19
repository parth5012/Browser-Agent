"""
Advanced configuration and utilities for the browser agent.
Provides additional setup options and helper functions.
"""

import os
import asyncio
from typing import Dict, Any, Optional, Callable
from enum import Enum
from dataclasses import dataclass, field

from logger_config import logger


class BrowserType(Enum):
    """Available browser types."""
    CHROMIUM = "chromium"
    FIREFOX = "firefox"
    WEBKIT = "webkit"


class ProxyMode(Enum):
    """Proxy configuration modes."""
    NONE = "none"
    HTTP = "http"
    SOCKS5 = "socks5"


@dataclass
class BrowserConfig:
    """Advanced browser configuration."""
    browser_type: BrowserType = BrowserType.CHROMIUM
    headless: bool = False
    proxy_mode: ProxyMode = ProxyMode.NONE
    proxy_url: Optional[str] = None
    
    # Visual settings
    viewport_width: int = 1280
    viewport_height: int = 720
    device_scale_factor: float = 1.0
    
    # Timeout settings
    navigation_timeout: int = 30000
    action_timeout: int = 10000
    script_timeout: int = 5000
    
    # Performance settings
    disable_blink_features: bool = False
    enable_video_recording: bool = False
    enable_network_monitoring: bool = False
    
    # Security settings
    verify_ssl: bool = True
    block_trackers: bool = True
    
    # Additional args
    extra_args: Dict[str, Any] = field(default_factory=dict)

    def to_playwright_config(self) -> Dict[str, Any]:
        """Convert to Playwright browser config."""
        return {
            "headless": self.headless,
            "args": self._get_args(),
            "device_scale_factor": self.device_scale_factor,
        }

    def _get_args(self) -> list[str]:
        """Get browser arguments."""
        args = []
        
        if self.disable_blink_features:
            args.append("--disable-blink-features=AutomationControlled")
        
        if self.block_trackers:
            args.append("--block-ads")
        
        if self.proxy_mode != ProxyMode.NONE and self.proxy_url:
            args.append(f"--proxy-server={self.proxy_url}")
        
        # Add custom args
        args.extend(self.extra_args.get("args", []))
        
        return args


@dataclass
class AgentConfig:
    """Advanced agent configuration."""
    model: str = "llama-3.3-70b-versatile"
    temperature: float = 0.7
    max_tokens: int = 2048
    top_p: float = 0.95
    top_k: int = 40
    
    # Agent behavior
    max_iterations: int = 10
    max_retries: int = 2
    timeout_per_iteration: int = 60
    
    # Tool configuration
    use_vision: bool = True
    enable_script_execution: bool = True
    max_screenshot_size: tuple[int, int] = (1280, 720)
    
    # Reasoning
    enable_chain_of_thought: bool = True
    enable_reflection: bool = True
    
    # Memory
    remember_history: bool = True
    max_history_length: int = 50


@dataclass
class SystemPrompt:
    """System prompt for the agent."""
    base: str = "You are an autonomous browser automation agent."
    
    instructions: list[str] = field(default_factory=lambda: [
        "Always take a screenshot first to see the current state",
        "Break down complex tasks into small steps",
        "Use CSS selectors to interact with elements",
        "Wait for dynamic content to load before interacting",
        "If something fails, try alternative approaches",
        "Provide clear explanations of what you're doing",
        "Stop when the task is complete",
    ])
    
    tools_description: str = """You have access to the following browser tools:
- navigate: Go to a URL
- take_screenshot: See what's on the screen
- click: Click on elements
- type: Type text into fields
- get_page_content: Get page HTML
- wait_for_element: Wait for elements to appear
- scroll: Scroll the page
- execute_javascript: Run JavaScript"""

    def build(self, task: str) -> str:
        """Build the complete system prompt."""
        prompt = self.base + "\n\n"
        
        prompt += self.tools_description + "\n\n"
        
        prompt += "IMPORTANT INSTRUCTIONS:\n"
        for i, instruction in enumerate(self.instructions, 1):
            prompt += f"{i}. {instruction}\n"
        
        prompt += f"\nCurrent task: {task}"
        
        return prompt


class AdvancedAgentConfig:
    """Advanced configuration manager."""

    def __init__(self):
        """Initialize advanced config."""
        self.browser_config = BrowserConfig()
        self.agent_config = AgentConfig()
        self.system_prompt = SystemPrompt()
        
        logger.info("Advanced configuration initialized")

    def load_from_env(self):
        """Load configuration from environment variables."""
        # Browser config from env
        if os.getenv("BROWSER_TYPE"):
            self.browser_config.browser_type = BrowserType(os.getenv("BROWSER_TYPE"))
        
        if os.getenv("HEADLESS"):
            self.browser_config.headless = os.getenv("HEADLESS").lower() == "true"
        
        if os.getenv("VIEWPORT_WIDTH"):
            self.browser_config.viewport_width = int(os.getenv("VIEWPORT_WIDTH"))
        
        if os.getenv("VIEWPORT_HEIGHT"):
            self.browser_config.viewport_height = int(os.getenv("VIEWPORT_HEIGHT"))
        
        # Agent config from env
        if os.getenv("MODEL_NAME"):
            self.agent_config.model = os.getenv("MODEL_NAME")
        
        if os.getenv("TEMPERATURE"):
            self.agent_config.temperature = float(os.getenv("TEMPERATURE"))
        
        if os.getenv("MAX_ITERATIONS"):
            self.agent_config.max_iterations = int(os.getenv("MAX_ITERATIONS"))
        
        logger.info("Configuration loaded from environment")

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "browser": {
                "type": self.browser_config.browser_type.value,
                "headless": self.browser_config.headless,
                "viewport": {
                    "width": self.browser_config.viewport_width,
                    "height": self.browser_config.viewport_height,
                },
            },
            "agent": {
                "model": self.agent_config.model,
                "temperature": self.agent_config.temperature,
                "max_iterations": self.agent_config.max_iterations,
            },
        }

    def save_config(self, filepath: str):
        """Save configuration to file."""
        import json
        try:
            with open(filepath, "w") as f:
                json.dump(self.to_dict(), f, indent=2)
            logger.info(f"Configuration saved to {filepath}")
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")

    def load_config(self, filepath: str):
        """Load configuration from file."""
        import json
        try:
            with open(filepath, "r") as f:
                config_dict = json.load(f)
            
            # Update configurations based on loaded data
            browser_config = config_dict.get("browser", {})
            if browser_config.get("type"):
                self.browser_config.browser_type = BrowserType(browser_config["type"])
            
            logger.info(f"Configuration loaded from {filepath}")
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")


class TaskExecutor:
    """Helper class for executing tasks with advanced options."""

    def __init__(self, agent):
        """Initialize task executor."""
        self.agent = agent
        self.config = AdvancedAgentConfig()

    async def execute_with_retry(
        self,
        task: str,
        max_retries: int = 3,
        backoff_factor: float = 1.5
    ) -> str:
        """Execute a task with automatic retry logic."""
        last_error = None
        
        for attempt in range(max_retries):
            try:
                logger.info(f"Attempt {attempt + 1}/{max_retries}")
                result = await self.agent.execute_task(task)
                return result
            except Exception as e:
                last_error = e
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                
                if attempt < max_retries - 1:
                    wait_time = backoff_factor ** attempt
                    logger.info(f"Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
        
        raise last_error

    async def execute_batch(self, tasks: list[str]) -> list[str]:
        """Execute multiple tasks sequentially."""
        results = []
        
        for i, task in enumerate(tasks, 1):
            logger.info(f"Executing task {i}/{len(tasks)}")
            try:
                result = await self.agent.execute_task(task)
                results.append(result)
            except Exception as e:
                logger.error(f"Task {i} failed: {e}")
                results.append(f"Error: {str(e)}")
        
        return results

    async def execute_parallel(self, tasks: list[str]) -> list[str]:
        """Execute multiple tasks in parallel."""
        logger.info(f"Executing {len(tasks)} tasks in parallel")
        
        results = await asyncio.gather(
            *[self.agent.execute_task(task) for task in tasks],
            return_exceptions=True
        )
        
        return results


# Example usage
if __name__ == "__main__":
    # Create config
    config = AdvancedAgentConfig()
    config.load_from_env()
    
    # Print configuration
    import json
    print(json.dumps(config.to_dict(), indent=2))
    
    # Save configuration
    config.save_config("agent_config.json")
