"""
Main LangGraph-based browser agent.
Orchestrates autonomous browser tasks using LangChain and Groq.
"""

import asyncio
import json
from typing import TypedDict, Optional, Annotated, Any
from enum import Enum

from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage, SystemMessage
from langchain_core.tools import BaseTool
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.types import Command

from browser_controller import BrowserController
from browser_tools import BrowserTools
from config import GROQ_API_KEY, MODEL_NAME, MAX_ITERATIONS, TEMPERATURE, HEADLESS, VIEWPORT_WIDTH, VIEWPORT_HEIGHT
from logger_config import logger


class AgentState(TypedDict):
    """State for the LangGraph agent."""
    messages: Annotated[list[BaseMessage], "The conversation messages"]
    task: str
    iterations: int
    max_iterations: int
    finished: bool
    result: Optional[str]


class BrowserAgent:
    """
    Autonomous browser agent using LangGraph and LangChain.
    Executes tasks in a browser using natural language instructions.
    """

    def __init__(self):
        """Initialize the browser agent."""
        self.browser_controller = BrowserController(
            headless=HEADLESS,
            viewport_width=VIEWPORT_WIDTH,
            viewport_height=VIEWPORT_HEIGHT,
        )
        
        self.llm = ChatGroq(
            api_key=GROQ_API_KEY,
            model_name=MODEL_NAME,
            temperature=TEMPERATURE,
            max_retries=2,
        )
        
        self.browser_tools = BrowserTools(self.browser_controller)
        self.tools = self.browser_tools.create_tools()
        
        self.graph = None
        self._setup_graph()
        
        logger.info(f"BrowserAgent initialized with model: {MODEL_NAME}")

    def _setup_graph(self):
        """Set up the LangGraph state machine."""
        workflow = StateGraph(AgentState)

        # Define nodes
        workflow.add_node("agent", self._agent_node)
        workflow.add_node("tools", ToolNode(self.tools))
        workflow.add_node("finish", self._finish_node)

        # Define edges
        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges(
            "agent",
            self._should_continue,
            {
                "continue": "tools",
                "finish": "finish",
            },
        )
        workflow.add_edge("tools", "agent")
        workflow.add_edge("finish", END)

        self.graph = workflow.compile()
        logger.info("LangGraph workflow compiled successfully")

    def _agent_node(self, state: AgentState) -> dict:
        """Process agent node - LLM decision making."""
        messages = state["messages"]
        
        # Prepare system message
        system_message = SystemMessage(
            content="""You are an autonomous browser automation agent. Your goal is to complete tasks by interacting with web browsers.

You have access to the following browser tools:
- navigate: Go to a URL
- take_screenshot: See what's on the screen
- click: Click on elements
- type: Type text into fields
- get_page_content: Get page HTML
- wait_for_element: Wait for elements to appear
- scroll: Scroll the page
- execute_javascript: Run JavaScript

IMPORTANT INSTRUCTIONS:
1. Always take a screenshot first to see the current state
2. Break down complex tasks into small steps
3. Use CSS selectors to interact with elements
4. Wait for dynamic content to load before interacting
5. If something fails, try alternative approaches
6. Provide clear explanations of what you're doing
7. Stop when the task is complete

Current task: """
            + state["task"]
        )

        # Invoke LLM with tools
        response = self.llm.bind_tools(self.tools).invoke(
            [system_message] + messages
        )

        state["messages"].append(response)
        state["iterations"] += 1

        logger.info(f"Agent iteration {state['iterations']}: {response.content[:100]}")

        return state

    def _should_continue(self, state: AgentState) -> str:
        """Determine if we should continue or finish."""
        if state["iterations"] >= state["max_iterations"]:
            logger.warning(f"Max iterations ({state['max_iterations']}) reached")
            return "finish"

        last_message = state["messages"][-1]

        # Check if there are tool calls
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "continue"

        # If no tool calls, we're done
        return "finish"

    def _finish_node(self, state: AgentState) -> dict:
        """Finalize the task."""
        last_message = state["messages"][-1]
        result = last_message.content if hasattr(last_message, "content") else str(last_message)
        
        state["finished"] = True
        state["result"] = result
        
        logger.info(f"Task finished. Result: {result[:200]}")
        
        return state

    async def execute_task(self, task: str, max_iterations: int = MAX_ITERATIONS) -> str:
        """
        Execute a task using the agent.
        
        Args:
            task: The task description
            max_iterations: Maximum iterations for the agent loop
            
        Returns:
            The task result
        """
        logger.info(f"Starting task: {task}")
        
        # Initialize browser
        await self.browser_controller.initialize()

        try:
            # Initialize state
            initial_state = AgentState(
                messages=[HumanMessage(content=task)],
                task=task,
                iterations=0,
                max_iterations=max_iterations,
                finished=False,
                result=None,
            )

            # Run the graph
            final_state = await asyncio.to_thread(
                self.graph.invoke,
                initial_state
            )

            result = final_state.get("result", "Task completed without explicit result")
            logger.info(f"Task completed: {result}")
            
            return result

        except Exception as e:
            logger.error(f"Task execution failed: {e}", exc_info=True)
            raise
        finally:
            await self.browser_controller.close()

    async def interactive_session(self):
        """Run an interactive session with the agent."""
        logger.info("Starting interactive session")
        
        await self.browser_controller.initialize()

        try:
            while True:
                task = input("\n🤖 Enter task (or 'quit' to exit): ").strip()
                
                if task.lower() == "quit":
                    logger.info("Interactive session ended")
                    break

                if not task:
                    continue

                result = await self.execute_task(task)
                print(f"\n✅ Result: {result}")

        except KeyboardInterrupt:
            logger.info("Interactive session interrupted")
        finally:
            await self.browser_controller.close()


async def main():
    """Main entry point."""
    agent = BrowserAgent()
    
    # Example task
    task = "Go to Google, search for 'LangChain browser automation', and tell me the first result"
    
    logger.info("=" * 60)
    logger.info("BROWSER AGENT - TASK EXECUTION")
    logger.info("=" * 60)
    
    result = await agent.execute_task(task)
    
    logger.info("=" * 60)
    logger.info(f"Final Result: {result}")
    logger.info("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
