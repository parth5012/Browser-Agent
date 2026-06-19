"""
LangChain tool definitions for browser automation.
These tools are used by the agent to interact with the browser.
"""

from typing import Optional
from langchain_core.tools import StructuredTool
from langchain_community.tools import tool
from pydantic import BaseModel, Field
from browser_controller import BrowserController
from logger_config import logger


class BrowserToolInput(BaseModel):
    """Input for browser tools."""
    pass


class NavigateInput(BrowserToolInput):
    """Input for navigation tool."""
    url: str = Field(description="The URL to navigate to")


class ClickInput(BrowserToolInput):
    """Input for click tool."""
    selector: str = Field(description="CSS selector of the element to click")


class TypeInput(BrowserToolInput):
    """Input for type tool."""
    selector: str = Field(description="CSS selector of the input element")
    text: str = Field(description="Text to type into the element")


class WaitInput(BrowserToolInput):
    """Input for wait tool."""
    selector: str = Field(description="CSS selector to wait for")
    timeout: int = Field(default=5000, description="Timeout in milliseconds")


class ScrollInput(BrowserToolInput):
    """Input for scroll tool."""
    direction: str = Field(default="down", description="Scroll direction: 'up' or 'down'")
    amount: int = Field(default=3, description="Number of times to scroll")


class ExecuteScriptInput(BrowserToolInput):
    """Input for script execution."""
    script: str = Field(description="JavaScript code to execute")


class BrowserTools:
    """Collection of browser automation tools for LangChain."""

    def __init__(self, browser_controller: BrowserController):
        """Initialize browser tools with a controller."""
        self.controller = browser_controller
        logger.info("BrowserTools initialized")

    @staticmethod
    def _make_sync(async_func):
        """Run an async function synchronously in a new event loop in a separate thread."""
        import asyncio
        import threading
        
        def wrapper(*args, **kwargs):
            res = []
            err = []
            def run():
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    res.append(loop.run_until_complete(async_func(*args, **kwargs)))
                except Exception as e:
                    err.append(e)
                finally:
                    loop.close()
            t = threading.Thread(target=run)
            t.start()
            t.join()
            if err:
                raise err[0]
            return res[0]
        return wrapper

    def create_tools(self) -> list[StructuredTool]:
        """Create and return all browser tools."""
        tools = [
            StructuredTool.from_function(
                name="navigate",
                func=self._make_sync(self._navigate),
                coroutine=self._navigate,
                description="Navigate to a URL in the browser. Use this to go to websites.",
                args_schema=NavigateInput,
            ),
            StructuredTool.from_function(
                name="take_screenshot",
                func=self._make_sync(self._take_screenshot),
                coroutine=self._take_screenshot,
                description="Take a screenshot of the current page. Use this to see what's on the screen.",
                args_schema=BrowserToolInput,
            ),
            StructuredTool.from_function(
                name="click",
                func=self._make_sync(self._click),
                coroutine=self._click,
                description="Click on an element using CSS selector. Useful for interacting with buttons, links, etc.",
                args_schema=ClickInput,
            ),
            StructuredTool.from_function(
                name="type",
                func=self._make_sync(self._type),
                coroutine=self._type,
                description="Type text into an input field or textarea. Provide selector and text.",
                args_schema=TypeInput,
            ),
            StructuredTool.from_function(
                name="get_page_content",
                func=self._make_sync(self._get_page_content),
                coroutine=self._get_page_content,
                description="Get the HTML content of the current page. Useful for analyzing page structure.",
                args_schema=BrowserToolInput,
            ),
            StructuredTool.from_function(
                name="wait_for_element",
                func=self._make_sync(self._wait_for_element),
                coroutine=self._wait_for_element,
                description="Wait for an element to appear on the page. Useful for handling dynamic content.",
                args_schema=WaitInput,
            ),
            StructuredTool.from_function(
                name="scroll",
                func=self._make_sync(self._scroll),
                coroutine=self._scroll,
                description="Scroll the page up or down. Useful for loading more content.",
                args_schema=ScrollInput,
            ),
            StructuredTool.from_function(
                name="execute_javascript",
                func=self._make_sync(self._execute_javascript),
                coroutine=self._execute_javascript,
                description="Execute arbitrary JavaScript code in the browser. Advanced use only.",
                args_schema=ExecuteScriptInput,
            ),
        ]
        logger.info(f"Created {len(tools)} browser tools")
        return tools

    async def _navigate(self, url: str) -> str:
        """Navigate to a URL."""
        try:
            result = await self.controller.navigate(url)
            return result.result if result.success else f"Error: {result.error}"
        except Exception as e:
            logger.error(f"Navigation error: {e}")
            return f"Error: {str(e)}"

    async def _take_screenshot(self) -> str:
        """Take a screenshot."""
        try:
            result = await self.controller.take_screenshot()
            return result.result if result.success else f"Error: {result.error}"
        except Exception as e:
            logger.error(f"Screenshot error: {e}")
            return f"Error: {str(e)}"

    async def _click(self, selector: str) -> str:
        """Click an element."""
        try:
            result = await self.controller.click(selector)
            return result.result if result.success else f"Error: {result.error}"
        except Exception as e:
            logger.error(f"Click error: {e}")
            return f"Error: {str(e)}"

    async def _type(self, selector: str, text: str) -> str:
        """Type text into an element."""
        try:
            result = await self.controller.type_text(selector, text)
            return result.result if result.success else f"Error: {result.error}"
        except Exception as e:
            logger.error(f"Type error: {e}")
            return f"Error: {str(e)}"

    async def _get_page_content(self) -> str:
        """Get page content."""
        try:
            result = await self.controller.get_page_content()
            return result.result if result.success else f"Error: {result.error}"
        except Exception as e:
            logger.error(f"Get page content error: {e}")
            return f"Error: {str(e)}"

    async def _wait_for_element(self, selector: str, timeout: int = 5000) -> str:
        """Wait for an element."""
        try:
            result = await self.controller.wait_for_selector(selector, timeout)
            return result.result if result.success else f"Error: {result.error}"
        except Exception as e:
            logger.error(f"Wait error: {e}")
            return f"Error: {str(e)}"

    async def _scroll(self, direction: str = "down", amount: int = 3) -> str:
        """Scroll the page."""
        try:
            result = await self.controller.scroll(direction, amount)
            return result.result if result.success else f"Error: {result.error}"
        except Exception as e:
            logger.error(f"Scroll error: {e}")
            return f"Error: {str(e)}"

    async def _execute_javascript(self, script: str) -> str:
        """Execute JavaScript."""
        try:
            result = await self.controller.execute_script(script)
            return result.result if result.success else f"Error: {result.error}"
        except Exception as e:
            logger.error(f"Script execution error: {e}")
            return f"Error: {str(e)}"
