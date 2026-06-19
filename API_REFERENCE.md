# Browser Agent - API Reference

## Core Classes

### BrowserAgent

Main class that orchestrates browser automation using LangGraph.

```python
from browser_agent import BrowserAgent

agent = BrowserAgent()
```

#### Methods

**`execute_task(task: str, max_iterations: int = 10) -> str`**
- Execute a task and get results
- **Args:**
  - `task`: Natural language task description
  - `max_iterations`: Maximum agent iterations
- **Returns:** Task result as string
- **Example:**
```python
result = await agent.execute_task("Search Google for Python")
```

**`interactive_session()`**
- Start interactive mode for continuous tasks
- **Example:**
```python
await agent.interactive_session()
```

---

### BrowserController

Low-level browser control and operations.

```python
from browser_controller import BrowserController

controller = BrowserController(headless=False)
```

#### Methods

**`initialize()`**
- Initialize the browser instance
- **Returns:** True if successful

**`navigate(url: str) -> BrowserAction`**
- Navigate to a URL
- **Args:** `url` - Target URL

**`take_screenshot() -> BrowserAction`**
- Capture current page screenshot
- **Returns:** BrowserAction with base64 image

**`click(selector: str) -> BrowserAction`**
- Click an element by CSS selector
- **Args:** `selector` - CSS selector string

**`type_text(selector: str, text: str) -> BrowserAction`**
- Type text into an element
- **Args:**
  - `selector` - CSS selector
  - `text` - Text to type

**`get_page_content() -> BrowserAction`**
- Get HTML content of current page
- **Returns:** HTML string

**`wait_for_selector(selector: str, timeout: int = 5000) -> BrowserAction`**
- Wait for element to appear
- **Args:**
  - `selector` - CSS selector
  - `timeout` - Timeout in milliseconds

**`scroll(direction: str = "down", amount: int = 3) -> BrowserAction`**
- Scroll the page
- **Args:**
  - `direction` - "up" or "down"
  - `amount` - Number of scroll times

**`execute_script(script: str) -> BrowserAction`**
- Execute JavaScript in browser
- **Args:** `script` - JavaScript code

**`close()`**
- Close the browser

#### Context Manager

```python
async with BrowserController(headless=False) as controller:
    await controller.navigate("https://example.com")
    # Auto-closes on exit
```

---

### BrowserTools

LangChain tool definitions for the agent.

```python
from browser_tools import BrowserTools
from browser_controller import BrowserController

controller = BrowserController()
tools = BrowserTools(controller)
browser_tools = tools.create_tools()
```

#### Available Tools

1. **navigate** - Go to URL
2. **take_screenshot** - Capture screen
3. **click** - Click element
4. **type** - Type text
5. **get_page_content** - Get HTML
6. **wait_for_element** - Wait for element
7. **scroll** - Scroll page
8. **execute_javascript** - Run JS

---

### AdvancedAgentConfig

Configuration management for advanced settings.

```python
from advanced_config import AdvancedAgentConfig

config = AdvancedAgentConfig()
config.load_from_env()
```

#### Properties

**`browser_config: BrowserConfig`**
- Browser-specific settings
- Properties:
  - `browser_type` - CHROMIUM, FIREFOX, WEBKIT
  - `headless` - bool
  - `viewport_width` - int
  - `viewport_height` - int

**`agent_config: AgentConfig`**
- Agent behavior settings
- Properties:
  - `model` - LLM model name
  - `temperature` - float (0-1)
  - `max_iterations` - int
  - `enable_vision` - bool

#### Methods

**`load_from_env()`**
- Load configuration from environment variables

**`save_config(filepath: str)`**
- Save configuration to JSON file

**`load_config(filepath: str)`**
- Load configuration from JSON file

**`to_dict() -> Dict`**
- Convert configuration to dictionary

---

### TaskExecutor

Helper for executing tasks with advanced options.

```python
from advanced_config import TaskExecutor
from browser_agent import BrowserAgent

agent = BrowserAgent()
executor = TaskExecutor(agent)
```

#### Methods

**`execute_with_retry(task: str, max_retries: int = 3) -> str`**
- Execute task with automatic retries
- **Args:**
  - `task` - Task description
  - `max_retries` - Number of retries

**`execute_batch(tasks: List[str]) -> List[str]`**
- Execute multiple tasks sequentially
- **Args:** `tasks` - List of task descriptions

**`execute_parallel(tasks: List[str]) -> List[str]`**
- Execute multiple tasks in parallel
- **Args:** `tasks` - List of task descriptions

---

## Data Classes

### BrowserAction

Result of a browser operation.

```python
from browser_controller import BrowserAction

@dataclass
class BrowserAction:
    success: bool
    result: Optional[str] = None
    error: Optional[str] = None
    screenshot: Optional[str] = None  # base64
```

### AgentState

State for LangGraph agent.

```python
@dataclass
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], "Conversation messages"]
    task: str
    iterations: int
    max_iterations: int
    finished: bool
    result: Optional[str]
```

---

## Configuration Objects

### BrowserConfig

```python
from advanced_config import BrowserConfig, BrowserType

config = BrowserConfig(
    browser_type=BrowserType.CHROMIUM,
    headless=False,
    viewport_width=1280,
    viewport_height=720,
    navigation_timeout=30000,
)
```

### AgentConfig

```python
from advanced_config import AgentConfig

config = AgentConfig(
    model="mixtral-8x7b-32768",
    temperature=0.7,
    max_iterations=10,
    enable_vision=True,
)
```

---

## Command Line Interface

### CLI Commands

**Run interactive mode:**
```bash
python main.py interactive
```

**Execute single task:**
```bash
python main.py task "Your task here"
```

**Execute batch tasks:**
```bash
python main.py batch tasks.json [--parallel]
```

**Show configuration:**
```bash
python main.py config [--show|--save FILE|--load FILE]
```

**Setup and verify:**
```bash
python main.py setup [--install|--browsers]
```

---

## Example Code

### Basic Usage

```python
import asyncio
from browser_agent import BrowserAgent

async def main():
    agent = BrowserAgent()
    result = await agent.execute_task(
        "Go to Google and search for Python"
    )
    print(result)

asyncio.run(main())
```

### Advanced Usage with Retry

```python
import asyncio
from advanced_config import TaskExecutor
from browser_agent import BrowserAgent

async def main():
    agent = BrowserAgent()
    executor = TaskExecutor(agent)
    
    result = await executor.execute_with_retry(
        "Extract data from website",
        max_retries=3
    )
    print(result)

asyncio.run(main())
```

### Batch Execution

```python
import asyncio
from advanced_config import TaskExecutor
from browser_agent import BrowserAgent

async def main():
    tasks = [
        "Search for Python",
        "Search for LangChain",
        "Search for Groq",
    ]
    
    agent = BrowserAgent()
    executor = TaskExecutor(agent)
    
    results = await executor.execute_batch(tasks)
    for task, result in zip(tasks, results):
        print(f"{task}: {result}")

asyncio.run(main())
```

### Custom Configuration

```python
from advanced_config import AdvancedAgentConfig

config = AdvancedAgentConfig()
config.browser_config.headless = True
config.browser_config.viewport_width = 1920
config.agent_config.temperature = 0.5
config.agent_config.max_iterations = 15

config.save_config("my_config.json")
```

---

## Environment Variables

### Required

- `GROQ_API_KEY` - Your Groq API key (get from https://console.groq.com)

### Optional

- `MODEL_NAME` - Groq model (default: mixtral-8x7b-32768)
- `TEMPERATURE` - LLM temperature 0-1 (default: 0.7)
- `MAX_ITERATIONS` - Max agent iterations (default: 10)
- `HEADLESS` - Run browser headless (default: false)
- `BROWSER_TIMEOUT` - Browser timeout in ms (default: 30000)
- `VIEWPORT_WIDTH` - Browser width (default: 1280)
- `VIEWPORT_HEIGHT` - Browser height (default: 720)
- `LOG_LEVEL` - Logging level (default: INFO)

---

## Error Handling

### Common Errors

```python
try:
    result = await agent.execute_task("task")
except KeyError as e:
    print(f"Configuration error: {e}")
except TimeoutError as e:
    print(f"Timeout: {e}")
except Exception as e:
    print(f"General error: {e}")
```

---

## Logging

Enable detailed logging:

```env
LOG_LEVEL=DEBUG
```

Access logs:
- Console: Real-time output
- File: `logs/browser_agent.log`

---

## Rate Limits

Groq API rate limits (check current limits):
- Free tier: Varies by model
- Paid: Higher limits available

Monitor usage and adjust `MAX_ITERATIONS` accordingly.

---

## Best Practices

1. **Error Handling**
```python
try:
    result = await agent.execute_task(task)
except Exception as e:
    logger.error(f"Task failed: {e}")
```

2. **Resource Management**
```python
async with BrowserController() as controller:
    # Browser automatically closes
    pass
```

3. **Task Description**
```python
# ❌ Avoid
await agent.execute_task("find stuff")

# ✅ Good
await agent.execute_task("Go to Google, search for 'Python libraries', and list top 3 results")
```

4. **Timeout Handling**
```python
config.browser_config.navigation_timeout = 60000
```

---

## Support & Resources

- **Documentation**: See README.md and QUICKSTART.md
- **Examples**: See examples.py
- **Issues**: Check logs in logs/browser_agent.log
- **API**: https://console.groq.com/docs
- **LangChain**: https://python.langchain.com/
- **LangGraph**: https://langgraph.js.org/

---

*Last updated: 2024*
