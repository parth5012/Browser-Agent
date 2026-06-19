#!/usr/bin/env python3
"""
Main CLI entry point for the Browser Agent.
Provides command-line interface for running tasks and examples.
"""

import asyncio
import sys
from typing import Optional
import argparse

from browser_agent import BrowserAgent
from advanced_config import AdvancedAgentConfig, TaskExecutor
from logger_config import logger


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        description="Browser Agent - Autonomous browser automation with LangChain & Groq",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run interactive mode
  python main.py interactive
  
  # Execute a single task
  python main.py task "Go to google.com and search for Python"
  
  # Run with custom configuration
  python main.py task "Visit example.com" --max-iterations 15
  
  # Batch execution
  python main.py batch tasks.json
  
  # Show configuration
  python main.py config
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Interactive command
    interactive_parser = subparsers.add_parser("interactive", help="Interactive mode")
    interactive_parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser in headless mode"
    )
    
    # Task command
    task_parser = subparsers.add_parser("task", help="Execute a single task")
    task_parser.add_argument(
        "task",
        type=str,
        help="Task description"
    )
    task_parser.add_argument(
        "--max-iterations",
        type=int,
        default=10,
        help="Maximum iterations for the agent (default: 10)"
    )
    task_parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="LLM temperature (default: 0.7)"
    )
    task_parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser in headless mode"
    )
    task_parser.add_argument(
        "--retry",
        type=int,
        default=1,
        help="Number of retries on failure (default: 1)"
    )
    
    # Batch command
    batch_parser = subparsers.add_parser("batch", help="Execute multiple tasks")
    batch_parser.add_argument(
        "file",
        type=str,
        help="JSON file with list of tasks"
    )
    batch_parser.add_argument(
        "--parallel",
        action="store_true",
        help="Execute tasks in parallel"
    )
    
    # Config command
    config_parser = subparsers.add_parser("config", help="Show/manage configuration")
    config_parser.add_argument(
        "--show",
        action="store_true",
        help="Show current configuration"
    )
    config_parser.add_argument(
        "--save",
        type=str,
        help="Save configuration to file"
    )
    config_parser.add_argument(
        "--load",
        type=str,
        help="Load configuration from file"
    )
    
    # Setup command
    setup_parser = subparsers.add_parser("setup", help="Setup and verify installation")
    setup_parser.add_argument(
        "--install",
        action="store_true",
        help="Install dependencies"
    )
    setup_parser.add_argument(
        "--browsers",
        action="store_true",
        help="Install Playwright browsers"
    )
    
    return parser


async def run_interactive(headless: bool = False):
    """Run interactive mode."""
    print("\n🤖 Browser Agent - Interactive Mode")
    print("=" * 60)
    print("Enter tasks or 'quit' to exit\n")
    
    agent = BrowserAgent()
    await agent.interactive_session()


async def run_task(
    task: str,
    max_iterations: int = 10,
    temperature: float = 0.7,
    headless: bool = False,
    retry: int = 1
):
    """Run a single task."""
    print("\n🤖 Browser Agent - Task Execution")
    print("=" * 60)
    print(f"Task: {task}\n")
    
    agent = BrowserAgent()
    executor = TaskExecutor(agent)
    
    try:
        if retry > 1:
            result = await executor.execute_with_retry(task, max_retries=retry)
        else:
            result = await agent.execute_task(task)
        
        print("\n✅ Task completed successfully!")
        print(f"\nResult:\n{result}")
    except Exception as e:
        print(f"\n❌ Task failed: {e}")
        logger.error(f"Task execution failed: {e}", exc_info=True)
        sys.exit(1)


async def run_batch(file_path: str, parallel: bool = False):
    """Run multiple tasks from a file."""
    import json
    
    print("\n🤖 Browser Agent - Batch Execution")
    print("=" * 60)
    
    try:
        with open(file_path, "r") as f:
            tasks = json.load(f)
        
        if not isinstance(tasks, list):
            print("❌ Tasks file must contain a JSON array")
            sys.exit(1)
        
        print(f"Loaded {len(tasks)} tasks\n")
        
        agent = BrowserAgent()
        executor = TaskExecutor(agent)
        
        if parallel:
            print("Executing tasks in parallel...\n")
            results = await executor.execute_parallel(tasks)
        else:
            print("Executing tasks sequentially...\n")
            results = await executor.execute_batch(tasks)
        
        print("\n" + "=" * 60)
        print("Batch Results:")
        print("=" * 60)
        
        for i, (task, result) in enumerate(zip(tasks, results), 1):
            print(f"\n[{i}] Task: {task[:50]}...")
            if isinstance(result, Exception):
                print(f"    ❌ Failed: {result}")
            else:
                print(f"    ✅ Success: {result[:100]}...")
    
    except FileNotFoundError:
        print(f"❌ Tasks file not found: {file_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON in tasks file")
        sys.exit(1)


def show_config():
    """Show configuration."""
    import json
    
    print("\n⚙️  Browser Agent - Configuration")
    print("=" * 60 + "\n")
    
    config = AdvancedAgentConfig()
    config.load_from_env()
    
    print(json.dumps(config.to_dict(), indent=2))


def save_config(file_path: str):
    """Save configuration to file."""
    print(f"\n💾 Saving configuration to {file_path}...")
    
    config = AdvancedAgentConfig()
    config.load_from_env()
    config.save_config(file_path)
    
    print("✅ Configuration saved")


def load_config(file_path: str):
    """Load configuration from file."""
    print(f"\n📂 Loading configuration from {file_path}...")
    
    config = AdvancedAgentConfig()
    config.load_config(file_path)
    
    print("✅ Configuration loaded")


def run_setup(install: bool = False, browsers: bool = False):
    """Run setup."""
    import setup
    
    if install or browsers:
        if install:
            print("📦 Installing dependencies...")
            setup.install_dependencies()
        
        if browsers:
            print("🌐 Installing Playwright browsers...")
            setup.install_playwright_browsers()
    else:
        setup.main()


async def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    try:
        if args.command == "interactive":
            await run_interactive(headless=args.headless)
        
        elif args.command == "task":
            await run_task(
                task=args.task,
                max_iterations=args.max_iterations,
                temperature=args.temperature,
                headless=args.headless,
                retry=args.retry
            )
        
        elif args.command == "batch":
            await run_batch(file_path=args.file, parallel=args.parallel)
        
        elif args.command == "config":
            if args.save:
                save_config(args.save)
            elif args.load:
                load_config(args.load)
            else:
                show_config()
        
        elif args.command == "setup":
            run_setup(install=args.install, browsers=args.browsers)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        logger.error(f"CLI error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
