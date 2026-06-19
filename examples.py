"""
Example tasks and use cases for the browser agent.
Demonstrates how to use the agent for various scenarios.
"""

import asyncio
from browser_agent import BrowserAgent
from logger_config import logger


class ExampleTasks:
    """Collection of example tasks for the browser agent."""

    @staticmethod
    async def example_1_web_search():
        """Example 1: Perform a web search."""
        agent = BrowserAgent()
        
        task = """
        1. Navigate to Google (google.com)
        2. Search for 'LangChain LangGraph browser automation'
        3. Extract the title of the first search result
        4. Return the title
        """
        
        logger.info("=" * 60)
        logger.info("EXAMPLE 1: Web Search")
        logger.info("=" * 60)
        
        result = await agent.execute_task(task)
        print(f"Result: {result}\n")

    @staticmethod
    async def example_2_form_filling():
        """Example 2: Fill and submit a form."""
        agent = BrowserAgent()
        
        task = """
        1. Navigate to a form (e.g., httpbin.org/forms/post)
        2. Fill in the form fields with sample data
        3. Submit the form
        4. Confirm submission was successful
        """
        
        logger.info("=" * 60)
        logger.info("EXAMPLE 2: Form Filling and Submission")
        logger.info("=" * 60)
        
        result = await agent.execute_task(task)
        print(f"Result: {result}\n")

    @staticmethod
    async def example_3_data_extraction():
        """Example 3: Extract data from a webpage."""
        agent = BrowserAgent()
        
        task = """
        1. Navigate to news.ycombinator.com
        2. Take a screenshot to see the page
        3. Extract the titles of the top 5 stories
        4. Return the list of titles
        """
        
        logger.info("=" * 60)
        logger.info("EXAMPLE 3: Data Extraction")
        logger.info("=" * 60)
        
        result = await agent.execute_task(task)
        print(f"Result: {result}\n")

    @staticmethod
    async def example_4_dynamic_content():
        """Example 4: Handle dynamic content with JavaScript."""
        agent = BrowserAgent()
        
        task = """
        1. Navigate to a page with dynamic content
        2. Wait for JavaScript to load content
        3. Extract the loaded data
        4. Return the extracted information
        """
        
        logger.info("=" * 60)
        logger.info("EXAMPLE 4: Dynamic Content Handling")
        logger.info("=" * 60)
        
        result = await agent.execute_task(task)
        print(f"Result: {result}\n")

    @staticmethod
    async def example_5_shopping():
        """Example 5: E-commerce automation."""
        agent = BrowserAgent()
        
        task = """
        1. Navigate to an e-commerce site (e.g., example.com/shop)
        2. Search for a specific product
        3. Find the product in the results
        4. Add it to cart
        5. Proceed to checkout
        6. Return the checkout page information
        """
        
        logger.info("=" * 60)
        logger.info("EXAMPLE 5: E-commerce Automation")
        logger.info("=" * 60)
        
        result = await agent.execute_task(task)
        print(f"Result: {result}\n")


async def run_all_examples():
    """Run all example tasks."""
    examples = [
        ExampleTasks.example_1_web_search,
        ExampleTasks.example_2_form_filling,
        ExampleTasks.example_3_data_extraction,
        ExampleTasks.example_4_dynamic_content,
        ExampleTasks.example_5_shopping,
    ]

    for example_func in examples:
        try:
            await example_func()
            await asyncio.sleep(2)  # Brief pause between examples
        except Exception as e:
            logger.error(f"Example failed: {e}")
            continue


async def run_single_example():
    """Run a single example task."""
    print("\n📋 Available Examples:")
    print("1. Web Search")
    print("2. Form Filling")
    print("3. Data Extraction")
    print("4. Dynamic Content")
    print("5. E-commerce")
    
    choice = input("\nSelect example (1-5): ").strip()
    
    examples = {
        "1": ExampleTasks.example_1_web_search,
        "2": ExampleTasks.example_2_form_filling,
        "3": ExampleTasks.example_3_data_extraction,
        "4": ExampleTasks.example_4_dynamic_content,
        "5": ExampleTasks.example_5_shopping,
    }
    
    if choice in examples:
        await examples[choice]()
    else:
        print("Invalid choice")


async def main():
    """Main entry point for examples."""
    print("\n🚀 Browser Agent - Example Tasks")
    print("=" * 60)
    print("Choose an option:")
    print("1. Run single example")
    print("2. Run all examples")
    print("3. Interactive mode")
    
    choice = input("\nSelect (1-3): ").strip()
    
    if choice == "1":
        await run_single_example()
    elif choice == "2":
        await run_all_examples()
    elif choice == "3":
        agent = BrowserAgent()
        await agent.interactive_session()
    else:
        print("Invalid choice")


if __name__ == "__main__":
    asyncio.run(main())
