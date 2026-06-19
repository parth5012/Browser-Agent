# Browser Agent - Architecture & Design Documentation

## 🏗️ System Architecture Overview

```
┌────────────────────────────────────────────────────────────────┐
│                    USER INTERFACE LAYER                         │
├────────────────────────────────────────────────────────────────┤
│  CLI (main.py)         │   Python API    │   Interactive Mode   │
└───────────┬─────────────────────────────┬──────────────────────┘
            │                             │
            └──────────────┬──────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                    AGENT ORCHESTRATION LAYER                    │
├──────────────────────────────────────────────────────────────────┤
│  BrowserAgent (browser_agent.py)                                 │
│  ├─ LangGraph Workflow                                           │
│  │  ├─ Agent Node (LLM Decision)                                │
│  │  ├─ Tool Node (Execute Actions)                              │
│  │  ├─ Finish Node (Results)                                    │
│  │  └─ Conditional Edges                                        │
│  ├─ State Management (AgentState)                               │
│  ├─ Task Execution Loop                                         │
│  └─ Error Handling & Recovery                                   │
└──────────────┬────────────────────────┬──────────────────────────┘
               │                        │
      ┌────────▼──────────┐    ┌────────▼──────────┐
      │   LLM LAYER       │    │   TOOLS LAYER     │
      │                   │    │                   │
```

## 🧠 LLM Layer

```
┌─────────────────────────────────────────┐
│        Groq API (ChatGroq)              │
│  Model: mixtral-8x7b-32768              │
│  Speed: Sub-1 second inference          │
│  Cost: Low                              │
│  Quality: High                          │
└────────────┬────────────────────────────┘
             │
      ┌──────▼─────────────────────┐
      │  LangChain Integration      │
      │  ├─ bind_tools()            │
      │  ├─ Message handling        │
      │  └─ Chain of thought        │
      └─────────────────────────────┘
```

## 🛠️ Tools Layer

```
┌────────────────────────────────────────────┐
│          BrowserTools (browser_tools.py)   │
├────────────────────────────────────────────┤
│                                            │
│  ┌──────────────────────────────────────┐  │
│  │  navigate(url)                       │  │
│  │  Click element by CSS selector       │  │
│  └──────────────────────────────────────┘  │
│                                            │
│  ┌──────────────────────────────────────┐  │
│  │  take_screenshot()                   │  │
│  │  Capture current page state          │  │
│  └──────────────────────────────────────┘  │
│                                            │
│  ┌──────────────────────────────────────┐  │
│  │  click(selector)                     │  │
│  │  Click element                       │  │
│  └──────────────────────────────────────┘  │
│                                            │
│  ┌──────────────────────────────────────┐  │
│  │  type(selector, text)                │  │
│  │  Type text into field                │  │
│  └──────────────────────────────────────┘  │
│                                            │
│  ┌──────────────────────────────────────┐  │
│  │  get_page_content()                  │  │
│  │  Extract HTML                        │  │
│  └──────────────────────────────────────┘  │
│                                            │
│  ┌──────────────────────────────────────┐  │
│  │  wait_for_element(selector)          │  │
│  │  Wait for dynamic content            │  │
│  └──────────────────────────────────────┘  │
│                                            │
│  ┌──────────────────────────────────────┐  │
│  │  scroll(direction, amount)           │  │
│  │  Scroll page                         │  │
│  └──────────────────────────────────────┘  │
│                                            │
│  ┌──────────────────────────────────────┐  │
│  │  execute_javascript(script)          │  │
│  │  Run custom JS                       │  │
│  └──────────────────────────────────────┘  │
│                                            │
└────────────┬───────────────────────────────┘
             │
             ▼
     ┌───────────────────┐
     │ BrowserController │
     └───────────────────┘
```

## 🌐 Browser Layer

```
┌─────────────────────────────────────────────────┐
│         BrowserController (browser_controller.py)│
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌──────────────────────────────────────────┐   │
│  │  Browser Instance                        │   │
│  │  ├─ Chromium / Firefox / WebKit          │   │
│  │  ├─ Viewport: 1280x720 (configurable)    │   │
│  │  ├─ Headless: false (default)            │   │
│  │  └─ Timeouts: 30s (configurable)         │   │
│  └──────────────────────────────────────────┘   │
│                                                  │
│  ┌──────────────────────────────────────────┐   │
│  │  Page Interactions                       │   │
│  │  ├─ Navigate                             │   │
│  │  ├─ Click                                │   │
│  │  ├─ Type                                 │   │
│  │  ├─ Scroll                               │   │
│  │  └─ Wait for elements                    │   │
│  └──────────────────────────────────────────┘   │
│                                                  │
│  ┌──────────────────────────────────────────┐   │
│  │  Screenshot & Analysis                   │   │
│  │  ├─ Capture viewport                     │   │
│  │  ├─ Encode to base64                     │   │
│  │  └─ Send to vision API                   │   │
│  └──────────────────────────────────────────┘   │
│                                                  │
│  ┌──────────────────────────────────────────┐   │
│  │  JavaScript Execution                    │   │
│  │  ├─ Get DOM content                      │   │
│  │  ├─ Extract data                         │   │
│  │  └─ Modify page                          │   │
│  └──────────────────────────────────────────┘   │
│                                                  │
└─────────────────────────────────────────────────┘
        │
        ▼ (via Playwright)
┌─────────────────────────────┐
│  Real Web Browser Instance  │
│  (Chromium/Firefox/WebKit)  │
│                             │
│  [Rendering Engine]         │
│  [JavaScript Runtime]       │
│  [DOM Tree]                 │
│  [CSS Engine]               │
└─────────────────────────────┘
```

## 🔄 Agent Loop Flow

```
START
  │
  ▼
┌─────────────────────────────────────┐
│  Take Screenshot                    │
│  (See current state)                │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Invoke LLM with:                   │
│  ├─ System prompt + task            │
│  ├─ Screenshots                     │
│  ├─ Previous actions                │
│  └─ Tool definitions                │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  LLM Decision:                      │
│  ├─ Analyze current state           │
│  ├─ Choose best tool                │
│  └─ Generate action plan            │
└────────────┬────────────────────────┘
             │
        ┌────┴─────────┐
        │              │
        ▼              ▼
   ┌─────────┐   ┌──────────┐
   │Tool Call│   │Task Done?│
   └────┬────┘   └─────┬────┘
        │              │
        ▼              ▼ (YES)
    ┌────────────┐   END
    │Execute Tool│   (Return Result)
    └────┬───────┘
        │
        ▼
  ┌──────────────┐
  │Wait for      │
  │completion &  │
  │observe result│
  └────┬─────────┘
        │
        ▼
    ┌──────────────────┐
    │Iteration count   │
    │< Max iterations? │
    └────┬──────┬──────┘
         │      │
       YES      NO
        │       │
        │       ▼
        │     END
        │   (Max reached)
        │
        └──────┘
             │
             ▼
    [Back to LLM Analysis]
```

## 📊 State Machine

```
AgentState
├─ messages: List[BaseMessage]
│  ├─ SystemMessage (instructions)
│  ├─ HumanMessage (task)
│  └─ AIMessage/ToolMessage (interaction history)
│
├─ task: str (task description)
│
├─ iterations: int (current iteration count)
│
├─ max_iterations: int (limit)
│
├─ finished: bool (task completion status)
│
└─ result: Optional[str] (final result)
```

## 🎯 Configuration Hierarchy

```
┌────────────────────────────────────────┐
│  AdvancedAgentConfig                   │
├────────────────────────────────────────┤
│                                        │
│  ├─ BrowserConfig                      │
│  │  ├─ browser_type (CHROMIUM)        │
│  │  ├─ headless (false)                │
│  │  ├─ viewport (1280x720)             │
│  │  ├─ timeouts (30s)                  │
│  │  └─ proxy settings                  │
│  │                                     │
│  ├─ AgentConfig                        │
│  │  ├─ model (mixtral-8x7b-32768)     │
│  │  ├─ temperature (0.7)               │
│  │  ├─ max_iterations (10)             │
│  │  ├─ enable_vision (true)            │
│  │  └─ other settings                  │
│  │                                     │
│  └─ SystemPrompt                       │
│     ├─ base instruction                │
│     ├─ tool descriptions               │
│     └─ custom guidelines               │
│                                        │
└────────────────────────────────────────┘
         ▲
         │ loads from
         │
    .env file
```

## 📁 Dependency Graph

```
browser_agent.py
├─ langchain_groq.ChatGroq
├─ langgraph.StateGraph
├─ browser_controller.BrowserController
├─ browser_tools.BrowserTools
├─ config.py (settings)
└─ logger_config.logger

browser_controller.py
├─ browser_use.Agent
├─ browser_use.Browser
├─ playwright
└─ logger_config.logger

browser_tools.py
├─ langchain.tools.Tool
├─ pydantic models
├─ browser_controller.BrowserController
└─ logger_config.logger

advanced_config.py
├─ dataclasses
├─ enum.Enum
├─ asyncio
└─ logger_config.logger

main.py
├─ browser_agent.BrowserAgent
├─ advanced_config
├─ argparse
└─ logger_config.logger

examples.py
├─ browser_agent.BrowserAgent
└─ logger_config.logger
```

## 🔐 Security Architecture

```
┌─────────────────────────────────────┐
│        Secure Credential Flow       │
├─────────────────────────────────────┤
│                                     │
│  .env (local only)                  │
│    │                                │
│    ▼                                │
│  python-dotenv                      │
│    │                                │
│    ▼                                │
│  Environment Variable               │
│    │                                │
│    ▼                                │
│  config.py (read only)              │
│    │                                │
│    ▼                                │
│  ChatGroq API (via SSL/TLS)         │
│                                     │
│  ✓ Never logged                     │
│  ✓ Never in code                    │
│  ✓ Never in git                     │
│  ✓ Only in memory                   │
│                                     │
└─────────────────────────────────────┘
```

## 🚀 Deployment Architecture

```
Development
├─ Local machine
├─ python main.py interactive
└─ View browser window

Production (Server)
├─ Headless mode (headless=true)
├─ Process manager (systemd/supervisor)
├─ Logging to files + remote
├─ API endpoint wrapper
└─ Task queue integration

Cloud (Docker)
├─ Base: Python 3.11
├─ Dependencies: requirements.txt
├─ Browsers: Playwright install
├─ Env: Environment variables
└─ Run: python main.py
```

## 📊 Performance Characteristics

```
Component            Typical Time    Range
─────────────────────────────────────────
LLM Inference        0.5-1.0s        0.3-2s
Screenshot Capture   0.2-0.5s        0.1-1s
DOM Click           0.1-0.3s        0.05-0.5s
Text Input          0.2-0.5s        0.1-1s
Page Navigation     1-3s            0.5-10s
Element Wait        0.5-5s          0.1-30s
Full Agent Loop     2-5s            1-15s

Parallel Execution: N tasks / (N/CPUs)
Batch Mode: N tasks * avg_time
```

## 🎓 Data Flow Example

```
User Input
  │
  ▼
Task: "Search Google for Python"
  │
  ▼
BrowserAgent.execute_task()
  │
  ├─► Initialize BrowserController
  │    ├─► Launch Chromium
  │    └─► Set viewport 1280x720
  │
  ├─► Start Agent Loop
  │    ├─► Take screenshot
  │    │    └─► Send to LLM with task
  │    │
  │    ├─► LLM responds:
  │    │   Action: navigate(url="https://google.com")
  │    │
  │    ├─► Execute Tool
  │    │    └─► Browser navigates
  │    │
  │    ├─► Iterate N times
  │    │    └─► Click search, type, submit, etc.
  │    │
  │    └─► LLM: "Task complete, result is..."
  │
  └─► Close Browser
        └─► Return Result
            │
            ▼
        "First result was..."
            │
            ▼
        Display to User
```

## 🔧 Extensibility Points

```
Custom Tools
├─ Add to BrowserTools.create_tools()
├─ Define schema with Pydantic
└─ Implement async function

Custom Nodes
├─ Add to workflow
├─ Implement node function
└─ Add edges

Custom LLM
├─ Replace ChatGroq
├─ Support langchain interface
└─ Configure in BrowserAgent.__init__

Custom Browser
├─ Extend BrowserController
├─ Override methods
└─ Support async operations

Custom Agent Logic
├─ Extend BrowserAgent
├─ Override _agent_node, _should_continue
└─ Customize graph structure
```

## 📈 Scaling Considerations

```
Single Agent       (1 browser)
├─ Max ~5-10 tasks/min
└─ Single process

Multi-Agent        (N browsers)
├─ Scale to 50-100 tasks/min
├─ Process pool/multiprocessing
└─ Shared task queue

Distributed        (Multiple servers)
├─ Scale to 1000+ tasks/min
├─ Message queue (Redis, RabbitMQ)
├─ Load balancing
└─ Database for state
```

---

## 🎯 Key Design Decisions

1. **LangGraph over direct agent code**
   - Reason: Better state management and workflow control

2. **Async throughout**
   - Reason: Better performance and resource utilization

3. **Modular architecture**
   - Reason: Easy to extend and test

4. **Configuration-driven**
   - Reason: Different settings for different use cases

5. **CLI + Python API**
   - Reason: Flexibility for different users

6. **Type hints**
   - Reason: Better code quality and IDE support

7. **Comprehensive logging**
   - Reason: Debugging and monitoring

---

*Architecture Document v1.0*
