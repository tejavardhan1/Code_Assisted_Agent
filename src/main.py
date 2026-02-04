import sys
import warnings

warnings.filterwarnings("ignore", category=Warning, module="langchain_core")

from langchain_core.messages import HumanMessage
from rich.console import Console
from rich.markdown import Markdown

from .agent import create_code_agent
from .version import __version__


def main():
    if len(sys.argv) > 1 and sys.argv[1] in ("-v", "--version"):
        print(__version__)
        return
    agent = create_code_agent()
    console = Console()
    console.print("[dim]Code Assistant. Type 'quit' to exit.[/dim]\n")
    while True:
        try:
            user_input = console.input("[bold green]> [/bold green]").strip()
            if not user_input:
                continue
            if user_input.lower() in ("quit", "exit", "q"):
                break
            result = agent.invoke({"messages": [HumanMessage(content=user_input)]})
            output = result["messages"][-1].content or ""
            console.print(Markdown(output))
        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[red]{e}[/red]")


if __name__ == "__main__":
    main()
