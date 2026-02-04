import os
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

from .tools import get_tools

SYSTEM_PROMPT = """You are a code assistant. You MUST use tools for all file operations.

Rules:
- List/read/search: ALWAYS call the tool. Never ask for clarification—use your best guess.
- Create file: use write_file with the full content. Never just output code.
- Search: use search_in_files with the given term. Try it even if vague.
- Be concise. Minimal changes."""


def create_code_agent():
    key = os.getenv("OPENAI_API_KEY", "")
    if key and "your" not in key.lower():
        llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=0,
            api_key=key,
        )
    else:
        llm = ChatOllama(model=os.getenv("OLLAMA_MODEL", "llama3.2"))
    graph = create_agent(
        model=llm,
        tools=get_tools(),
        system_prompt=SYSTEM_PROMPT,
    )
    return graph
