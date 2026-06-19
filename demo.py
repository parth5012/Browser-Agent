#!/usr/bin/env python3
"""
Browser Agent - DEMO MODE
Shows the agent in action with mock responses
"""
import asyncio
from typing import TypedDict, Annotated, Optional
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

print("\n" + "="*70)
print("  BROWSER AGENT - DEMO MODE")
print("="*70)
print("\nThis is a demonstration of the agent without needing an API key.")
print("The agent will show its reasoning process and mock browser actions.\n")

class DemoAgentState(TypedDict):
    """Demo agent state"""
    messages: Annotated[list[BaseMessage], "Messages"]
    task: str
    step: int
    result: Optional[str]

class DemoAgent:
    """Simplified demo agent for demonstration"""
    
    def __init__(self):
        self.graph = None
        self._setup_graph()
    
    def _setup_graph(self):
        """Set up the demo agent"""
        workflow = StateGraph(DemoAgentState)
        
        workflow.add_node("analyze", self._analyze)
        workflow.add_node("execute", self._execute)
        workflow.add_node("finish", self._finish)
        
        workflow.add_edge(START, "analyze")
        workflow.add_conditional_edges(
            "analyze",
            self._should_continue,
            {
                "continue": "execute",
                "finish": "finish",
            }
        )
        workflow.add_edge("execute", "analyze")
        workflow.add_edge("finish", END)
        
        self.graph = workflow.compile()
    
    def _analyze(self, state: DemoAgentState) -> dict:
        """Analyze state (simulated LLM thinking)"""
        step = state["step"]
        task = state["task"]
        
        print(f"\n[Step {step + 1}] Agent Thinking...")
        print(f"  Task: {task}")
        
        messages = state["messages"].copy()
        
        # Simulate LLM reasoning
        if "google" in task.lower():
            if step == 0:
                thought = "I need to navigate to Google first"
                messages.append(AIMessage(content=thought))
                print(f"  Thought: {thought}")
            elif step == 1:
                thought = "Now I'll search for the term"
                messages.append(AIMessage(content=thought))
                print(f"  Thought: {thought}")
            elif step == 2:
                thought = "Task complete - search results displayed"
                messages.append(AIMessage(content=thought))
                print(f"  Thought: {thought}")
                return {
                    **state,
                    "messages": messages,
                    "step": step + 1,
                    "result": "Task completed successfully"
                }
        
        return {
            **state,
            "messages": messages,
            "step": step + 1,
        }
    
    def _execute(self, state: DemoAgentState) -> dict:
        """Execute browser action (simulated)"""
        step = state["step"]
        task = state["task"]
        
        actions = [
            "Navigating to https://google.com",
            "Clicking search box",
            "Typing query",
            "Pressing Enter",
            "Analyzing results",
        ]
        
        if step - 1 < len(actions):
            action = actions[min(step - 1, len(actions) - 1)]
            print(f"  [Browser] {action}")
        
        return state
    
    def _should_continue(self, state: DemoAgentState) -> str:
        """Should continue or finish"""
        if state["step"] >= 3:
            return "finish"
        return "continue"
    
    def _finish(self, state: DemoAgentState) -> dict:
        """Finish task"""
        print(f"\n[Complete] Task finished!")
        print(f"  Result: {state['result']}")
        return state
    
    async def run(self, task: str):
        """Run the demo agent"""
        initial_state = DemoAgentState(
            messages=[HumanMessage(content=task)],
            task=task,
            step=0,
            result=None,
        )
        
        final_state = await asyncio.to_thread(
            self.graph.invoke,
            initial_state
        )
        
        return final_state.get("result")

async def demo():
    """Run demo"""
    print("="*70)
    print("  DEMO 1: Web Search Task")
    print("="*70)
    
    agent = DemoAgent()
    task = "Go to Google and search for 'LangChain browser automation'"
    result = await agent.run(task)
    
    print("\n" + "="*70)
    print("  AGENT CAPABILITIES")
    print("="*70 + "\n")
    
    print("The agent can perform these browser operations:")
    print("  1. navigate(url) - Go to websites")
    print("  2. click(selector) - Click elements")
    print("  3. type(selector, text) - Type text")
    print("  4. take_screenshot() - Capture pages")
    print("  5. scroll(direction) - Scroll pages")
    print("  6. wait_for_element() - Wait for content")
    print("  7. get_page_content() - Extract HTML")
    print("  8. execute_javascript() - Run JS")
    
    print("\n" + "="*70)
    print("  TO RUN WITH REAL BROWSER:")
    print("="*70 + "\n")
    
    print("1. Get Groq API key: https://console.groq.com (free)")
    print("2. Edit .env file:")
    print("   GROQ_API_KEY=your_api_key_here")
    print("3. Run interactive mode:")
    print("   python main.py interactive")
    print("\n4. Or execute a single task:")
    print("   python main.py task \"Search Google for Python\"")
    
    print("\n" + "="*70)
    print("  QUICK COMMANDS:")
    print("="*70 + "\n")
    
    print("python main.py interactive    # Chat with agent")
    print("python main.py task \"task\"    # Execute one task")
    print("python main.py batch file.json # Batch processing")
    print("python main.py config --show   # Show configuration")
    
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    asyncio.run(demo())
