# 🤖 Browser Agent - LangGraph + LangChain + Groq

A complete autonomous browser automation agent built with **LangGraph**, **LangChain**, and **Groq API**. The agent can understand natural language instructions and perform complex tasks in a web browser autonomously.

## 🎯 Features

- **🧠 AI-Powered**: Uses Groq's fast Mixtral model for reasoning
- **🔄 Autonomous**: Runs agent loops with tool use and reflection
- **🌐 Web Automation**: Full browser control (navigate, click, type, screenshot, etc.)
- **🛠️ Tool-Based**: 8+ integrated browser tools
- **📊 State Management**: LangGraph for robust workflow orchestration
- **🔍 Vision Support**: Screenshot analysis for intelligent decision-making
- **⚡ Fast**: Groq API provides sub-second inference
- **📝 Logging**: Comprehensive logging with loguru

## 📋 Requirements

- Python 3.10+
- Groq API Key (get free at https://console.groq.com)
- Playwright (for browser automation)

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or create project directory
cd "D:\work\projects\Browsser Agent"

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

### 2. Configuration

Edit `.env` file with your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
HEADLESS=false
```

### 3. Run Examples

```bash
# Interactive mode
python examples.py

# Single task
python browser_agent.py

# Direct execution
python -c "
import asyncio
from browser_agent import BrowserAgent

async def main():
    agent = BrowserAgent()
    result = await agent.execute_task('Go to Google and search for Python')
    print(result)

asyncio.run(main())
"
```

## 🏗️ Architecture

```
browser_agent.py
├── BrowserAgent (LangGraph orchestrator)
├── State Management
├── Agent Nodes
│   ├── agent_node (LLM reasoning)
│   ├── tools_node (Tool execution)
│   └── finish_node (Results)
└── Conditional Edges

browser_controller.py
└── BrowserController
    ├── Browser initialization
    ├── Screenshot capture
    ├── DOM interaction
    └── JavaScript execution

browser_tools.py
└── BrowserTools (LangChain Tools)
    ├── navigate
    ├── take_screenshot
    ├── click
    ├── type
    ├── get_page_content
    ├── wait_for_element
    ├── scroll
    └── execute_javascript
```

## 📚 Available Tools

### 1. Navigate
Navigate to a URL
```python
await agent.execute_task("Go to https://example.com")
```

### 2. Take Screenshot
Capture the current page
```python
await agent.execute_task("Take a screenshot of the current page")
```

### 3. Click
Click on elements using CSS selectors
```python
await agent.execute_task("Click the submit button")
```

### 4. Type
Type text into input fields
```python
await agent.execute_task("Type 'hello world' into the search box")
```

### 5. Get Page Content
Extract HTML content
```python
await agent.execute_task("Get the page content and analyze it")
```

### 6. Wait for Element
Wait for elements to appear
```python
await agent.execute_task("Wait for the results to load")
```

### 7. Scroll
Scroll the page
```python
await agent.execute_task("Scroll down to see more content")
```

### 8. Execute JavaScript
Run custom JavaScript
```python
await agent.execute_task("Run JavaScript to get all links")
```

## 💡 Usage Examples

### Example 1: Web Search
```python
import asyncio
from browser_agent import BrowserAgent

async def main():
    agent = BrowserAgent()
    task = """
    1. Navigate to Google
    2. Search for 'LangChain'
    3. Return the first 3 results
    """
    result = await agent.execute_task(task)
    print(result)

asyncio.run(main())
```

### Example 2: Form Filling
```python
async def fill_form():
    agent = BrowserAgent()
    task = """
    1. Go to the contact form
    2. Fill Name: John Doe
    3. Fill Email: john@example.com
    4. Fill Message: Hello, this is a test
    5. Submit the form
    6. Confirm success
    """
    result = await agent.execute_task(task)
    print(result)
```

### Example 3: Data Extraction
```python
async def extract_data():
    agent = BrowserAgent()
    task = """
    1. Navigate to news.ycombinator.com
    2. Extract top 10 story titles
    3. Get the score for each story
    4. Return as a formatted list
    """
    result = await agent.execute_task(task)
    print(result)
```

### Example 4: Interactive Session
```python
import asyncio
from browser_agent import BrowserAgent

async def main():
    agent = BrowserAgent()
    await agent.interactive_session()

asyncio.run(main())
```

## 🔧 Configuration Options

Edit `.env` to customize behavior:

```env
# Groq Configuration
GROQ_API_KEY=your_key_here
MODEL_NAME=mixtral-8x7b-32768  # or other Groq models
TEMPERATURE=0.7

# Browser Settings
HEADLESS=false                 # Set to true for headless mode
BROWSER_TIMEOUT=30000          # Timeout in milliseconds
VIEWPORT_WIDTH=1280
VIEWPORT_HEIGHT=720

# Agent Settings
MAX_ITERATIONS=10              # Maximum agent loop iterations
LOG_LEVEL=INFO                 # DEBUG, INFO, WARNING, ERROR
```

## 🎓 How It Works

1. **Task Input**: User provides a natural language task
2. **Agent Loop**: 
   - LLM analyzes the task and current state
   - Decides which tool to use
   - Executes the tool
   - Observes the result
   - Repeats until task is complete
3. **Screenshot Analysis**: Agent can "see" the browser
4. **Tool Usage**: Tools handle specific browser operations
5. **Result**: Final result is returned to the user

## 🤖 Agent Decision Flow

```
┌─────────────────────┐
│   Receive Task      │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│   Take Screenshot   │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│   LLM Analyzes      │◄──── Current State
│   (using LangChain) │
└────────┬────────────┘
         │
    ┌────┴─────┐
    │           │
    ▼           ▼
┌────────┐  ┌──────────┐
│ Tool   │  │ Task     │
│ Call   │  │ Complete?│
└─┬──────┘  └──────┬───┘
  │                │
  └────────┬───────┘
           │
         ┌─┴─┐
         │   │
        YES  NO
         │   │
         ▼   ▼
      DONE REPEAT
```

## 📊 Logging

Logs are saved to `logs/browser_agent.log` and printed to console:

```
INFO | browser_agent:_agent_node:84 - Agent iteration 1: Taking screenshot to see current state
INFO | browser_controller:navigate:79 - Navigating to: https://google.com
DEBUG | browser_tools:_click:143 - Clicking element: input[name="q"]
```

## 🐛 Debugging

### Enable Debug Logging
```env
LOG_LEVEL=DEBUG
```

### Check Browser State
```python
# The agent will automatically take screenshots
# Check logs for screenshot URLs
```

### Inspect Tool Calls
```python
# View in logs what tools are being called and their results
```

## ⚠️ Limitations & Best Practices

### Current Limitations
- Browser-use integration requires proper setup
- Some JavaScript-heavy sites may need additional wait time
- CAPTCHA challenges are not automatically handled

### Best Practices
1. **Be Descriptive**: Provide clear, detailed task instructions
2. **Break Down Tasks**: Complex tasks work better when split into steps
3. **Use Specific Selectors**: Provide CSS selectors when possible
4. **Handle Timeouts**: Add explicit wait instructions for slow-loading content
5. **Test First**: Test with simple tasks before complex automation
6. **Monitor Usage**: Groq API has rate limits, monitor your usage

## 🔐 Security

- Never commit `.env` with real API keys
- Use environment variables for sensitive data
- Validate user input before executing
- Be cautious with `execute_javascript` tool
- Monitor logs for security issues

## 🤝 Extending the Agent

### Add Custom Tools

```python
from langchain.tools import Tool

def my_custom_tool(param: str) -> str:
    # Your implementation
    return result

# Add to BrowserTools.create_tools()
```

### Add Custom Nodes

```python
def custom_node(state: AgentState) -> dict:
    # Your logic
    return state

# Add to workflow in _setup_graph()
```

### Use Different LLM

```python
from langchain_openai import ChatOpenAI
# Or other providers
```

## 📦 Project Structure

```
browser-agent/
├── browser_agent.py          # Main agent
├── browser_controller.py      # Browser control
├── browser_tools.py           # LangChain tools
├── config.py                  # Configuration
├── logger_config.py           # Logging setup
├── examples.py                # Example tasks
├── requirements.txt           # Dependencies
├── .env                       # Environment variables
├── README.md                  # This file
└── logs/                      # Log files
```

## 🚀 Deployment

### Local Development
```bash
python browser_agent.py
```

### Server Deployment
```bash
# Run as background process
nohup python browser_agent.py > output.log 2>&1 &
```

### Docker (Optional)
```dockerfile
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN playwright install
CMD ["python", "browser_agent.py"]
```

## 📞 Support

For issues:
1. Check logs in `logs/browser_agent.log`
2. Verify Groq API key is valid
3. Ensure Playwright is installed: `playwright install`
4. Check Python version: `python --version`

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Credits

Built with:
- [LangChain](https://python.langchain.com/)
- [LangGraph](https://langgraph.js.org/)
- [Groq](https://groq.com/)
- [browser-use](https://github.com/browser-use/browser-use)
- [Playwright](https://playwright.dev/)

---

**Happy automating! 🎉**
