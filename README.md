# AI Agent (Python)

A toy AI coding agent built with the Google Gemini API. It can explore a working directory, read files, write files, and execute Python scripts in a sandboxed location to iteratively complete tasks.

## Features
- Function calling via Gemini's tool API
- Iterative agent loop with bounded iterations
- Tools: get_files_info, get_file_content, write_file, run_python_file

## Setup
1. Install dependencies with `uv sync`
2. Add your `GEMINI_API_KEY` to a `.env` file
3. Set `WORKING_DIRECTORY` in `config.py`
4. Run: `uv run main.py "your prompt here"`

## Project Structure
- `main.py` — entry point and agent loop
- `functions/` — tool implementations
- `call_function.py` — dispatches function calls from the model
- `prompts.py` — system prompt
- `config.py` — configuration constants
