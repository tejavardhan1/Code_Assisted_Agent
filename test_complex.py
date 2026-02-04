"""Run a complex multi-step task against the agent."""
import warnings
warnings.filterwarnings("ignore", category=Warning, module="langchain_core")

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from rich.console import Console
from rich.panel import Panel

load_dotenv()

PROMPT = """Create examples/counter.py with a function count_lines(file_path: str) -> int that returns the number of lines in the file.
Add a main block that calls count_lines('examples/sample.py') and prints the result.
Then read README.md and add a line under the Structure section: '- examples/counter.py - line counter util'"""


def run():
    from src.agent import create_code_agent

    agent = create_code_agent()
    console = Console()
    os.chdir(Path(__file__).parent)
    console.print(Panel(PROMPT, title="Complex Task", border_style="yellow"))
    try:
        result = agent.invoke({"messages": [HumanMessage(content=PROMPT)]})
        output = str(result["messages"][-1].content or "")
        console.print(output)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    run()
