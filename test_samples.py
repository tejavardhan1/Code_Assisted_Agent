import warnings
warnings.filterwarnings("ignore", category=Warning, module="langchain_core")

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from rich.console import Console
from rich.panel import Panel

load_dotenv()

SAMPLES = [
    "List all files in the current directory.",
    "Read requirements.txt and tell me the main dependencies.",
    "Search for 'create_agent' in the codebase.",
    "What does src/agent.py do? Summarize briefly.",
    "Create examples/hello.py that prints 'Hello, World!'",
    "Read the README and tell me how to run this agent.",
]


def run():
    from src.agent import create_code_agent

    agent = create_code_agent()
    console = Console()
    root = Path(__file__).parent
    os.chdir(root)

    for i, prompt in enumerate(SAMPLES, 1):
        console.print(Panel(f"[bold]{prompt}[/bold]", title=f"Sample {i}/{len(SAMPLES)}", border_style="blue"))
        try:
            result = agent.invoke({"messages": [HumanMessage(content=prompt)]})
            output = str(result["messages"][-1].content or "")
            console.print(output[:2000] + ("..." if len(output) > 2000 else ""))
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
        console.print()


if __name__ == "__main__":
    run()
