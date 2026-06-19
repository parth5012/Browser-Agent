# 🚀 Browser Agent - Quick Start Guide

## 📌 What is the Browser Agent?

A fully autonomous browser automation system powered by **LangGraph**, **LangChain**, and **Groq API**. It uses AI to understand natural language tasks and execute them in a web browser automatically.

### Key Features:
- 🧠 **AI-Powered Decision Making** - Uses Groq's fast Mixtral model
- 🔄 **Autonomous Loops** - Self-correcting agent that learns from actions
- 🌐 **Full Browser Control** - Navigate, click, type, scroll, analyze
- 📸 **Vision Capabilities** - Understands what's on screen
- ⚡ **Fast & Efficient** - Groq inference is sub-second
- 🛠️ **8+ Built-in Tools** - Navigate, click, type, wait, scroll, etc.

## ⏱️ 5-Minute Setup

### Step 1: Get Groq API Key (1 min)
1. Go to https://console.groq.com
2. Sign up (free)
3. Copy your API key

### Step 2: Clone/Setup Project (1 min)
```bash
cd "D:\work\projects\Browsser Agent"
```

### Step 3: Install Dependencies (2 min)
```bash
# Install Python packages
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

### Step 4: Configure API Key (1 min)
Edit `.env` file:
```env
GROQ_API_KEY=your_api_key_here
```

Done! ✅

## 🎯 Your First Task (2 minutes)

### Option 1: Quick Command
```bash
python main.py task "Go to Google and search for Python programming"
```

### Option 2: Interactive Mode
```bash
python main.py interactive
```
Then type your tasks!

### Option 3: Python Script
```python
import asyncio
from browser_agent import BrowserAgent

async def main():
    agent = BrowserAgent()
    result = await agent.execute_task(
        "Go to Google and search for 'LangChain'"
    )
    print(result)

asyncio.run(main())
```

## 📚 Common Tasks

### Search the Web
```bash
python main.py task "Search Google for 'best Python libraries'"
```

### Extract Data
```bash
python main.py task "Go to news.ycombinator.com and get top 5 story titles"
```

### Fill Forms
```bash
python main.py task "
1. Go to contact form
2. Fill name: John Doe
3. Fill email: john@example.com
4. Submit
"
```

### Data Collection
```bash
python main.py task "
1. Navigate to Wikipedia
2. Search for 'Machine Learning'
3. Extract the first 2 paragraphs
"
```

## 🎮 Advanced Usage

### With Retries
```bash
python main.py task "Your task" --retry 3
```

### Custom Iterations
```bash
python main.py task "Your task" --max-iterations 20
```

### Batch Execution
```bash
python main.py batch sample_tasks.json
```

### Parallel Execution
```bash
python main.py batch sample_tasks.json --parallel
```

### Interactive Session
```bash
python main.py interactive
```

## 🛠️ Architecture

```
Task (Natural Language)
        ↓
    Agent Loop (LangGraph)
        ↓
    ├─ Analyze with LLM
    ├─ Decide tool
    ├─ Execute tool
    ├─ Observe result
    └─ Repeat or Finish
        ↓
    Result (Text/Data)
```

## 📖 Available Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `navigate` | Go to URL | "Go to google.com" |
| `click` | Click element | "Click the search button" |
| `type` | Type text | "Type 'hello' in the search box" |
| `take_screenshot` | See screen | "Take a screenshot" |
| `wait_for_element` | Wait for element | "Wait for results to load" |
| `scroll` | Scroll page | "Scroll down" |
| `get_page_content` | Get HTML | "Extract all links" |
| `execute_javascript` | Run JS | "Get page title" |

## 📁 Project Structure

```
browser-agent/
├── browser_agent.py          # Main agent (LangGraph)
├── browser_controller.py      # Browser operations
├── browser_tools.py           # LangChain tools
├── advanced_config.py         # Configuration
├── main.py                    # CLI interface
├── examples.py                # Example tasks
├── setup.py                   # Setup utility
├── requirements.txt           # Dependencies
├── .env                       # Configuration
├── sample_tasks.json          # Sample batch tasks
└── README.md                  # Full documentation
```

## 🔧 Configuration

### Quick Config (.env)
```env
GROQ_API_KEY=your_key          # Required!
HEADLESS=false                 # Show browser
MODEL_NAME=mixtral-8x7b-32768  # Groq model
TEMPERATURE=0.7                # LLM creativity
MAX_ITERATIONS=10              # Max agent steps
```

### Advanced Config
See `advanced_config.py` for browser types, timeouts, and more.

## 📊 Examples

### Example 1: Web Search ⌕
```python
task = "Search Google for 'OpenAI GPT' and get the first result"
result = await agent.execute_task(task)
# Returns: Title and link of first result
```

### Example 2: Data Extraction 📊
```python
task = """
Go to Hacker News:
1. Extract top 10 story titles
2. Get score for each
3. Return as list
"""
result = await agent.execute_task(task)
```

### Example 3: Form Submission 📝
```python
task = """
Fill contact form at example.com:
1. Name: Jane Doe
2. Email: jane@example.com
3. Message: Interested in your service
4. Submit
"""
result = await agent.execute_task(task)
```

## ⚡ Performance Tips

1. **Be Specific**: Clear instructions = faster execution
2. **Use Selectors**: Provide CSS selectors when possible
3. **Add Waits**: Wait for dynamic content to load
4. **Test First**: Test with simple tasks
5. **Monitor API**: Groq has rate limits

## 🐛 Troubleshooting

### Error: "GROQ_API_KEY not set"
**Solution**: 
```bash
# Edit .env file and add your API key
GROQ_API_KEY=gsk_...
```

### Error: "Browser not initialized"
**Solution**:
```bash
# Install Playwright browsers
playwright install
```

### Task Timeout
**Solution**:
```bash
# Increase timeout in .env
BROWSER_TIMEOUT=60000
```

### No Results
**Solution**:
```bash
# Increase iterations
python main.py task "Your task" --max-iterations 15
```

## 📞 Support

1. Check logs in `logs/browser_agent.log`
2. Enable debug mode: `LOG_LEVEL=DEBUG` in .env
3. Read `README.md` for detailed docs
4. Check browser window (if headless=false)

## 🎓 Learn More

- [LangChain Docs](https://python.langchain.com/)
- [LangGraph Docs](https://langgraph.js.org/)
- [Groq Console](https://console.groq.com/)
- [Playwright Docs](https://playwright.dev/)

## 📋 Checklist

- [ ] Python 3.10+ installed
- [ ] Groq API key obtained
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Playwright browsers installed (`playwright install`)
- [ ] .env configured with API key
- [ ] First task executed successfully

## 🎉 Next Steps

1. ✅ Run your first task
2. ✅ Try batch execution
3. ✅ Create custom tasks
4. ✅ Integrate into your application
5. ✅ Build automation workflows

---

**Ready to automate?** Run your first task:
```bash
python main.py task "Go to google.com"
```

Happy automating! 🚀
