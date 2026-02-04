# Code Assistant Agent v0.1.0

AI agent that reads, writes, searches, and modifies code via LLM tool-calling. Built with LangChain. Runs locally with Ollama.

**Tools:** read_file, write_file, list_directory, search_in_files

## Setup

```bash
pip install -r requirements.txt
ollama pull llama3.2
```

## Run

```bash
python3 -m src.main
```

Optional: `export OLLAMA_MODEL=llama3.1:8b` to use a different model.

## Test

```bash
python3 test_samples.py
python3 test_complex.py
```

## Structure

```
src/
  agent.py      # Agent + Ollama
  main.py       # CLI
  version.py
  tools/        # read, write, list, search
examples/
  counter.py
```
