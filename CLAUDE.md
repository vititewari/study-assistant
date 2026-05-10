# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A study assistant CLI powered by Claude (Anthropic SDK) with tool use. The assistant can save/search study notes via tools that Claude calls autonomously during conversation.

## Commands

```powershell
# Activate venv (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Run the assistant
python main.py
```

## Architecture

The app follows the Claude tool-use pattern:

- **`main.py`** — entry point; sets up the Anthropic client, registers tools, and runs the conversation loop
- **`tools/notes.py`** — note-taking tool: reads/writes `data/notes.txt`
- **`tools/search.py`** — search tool: queries notes or external sources
- **`data/notes.txt`** — flat-file persistent storage for study notes

### Tool registration

Tool schemas are defined manually as Python dictionaries (not generated from docstrings) and passed to `client.messages.create(tools=[...])`. The tool call loop processes `tool_use` content blocks in Claude's response, dispatches to the matching function, and feeds results back as `tool_result` messages.

## Code rules

- All tool functions must have docstrings.
- Tool functions must catch exceptions internally and return an error string — never raise to the caller.
- Never use `print()` for errors — use `return` with an error string.
- Notes are persisted to `data/notes.txt` (relative to the project root).
- After implementing any new feature, run `python main.py` and verify it works before reporting done.

## Windows notes

- Run on Windows PowerShell; avoid `<`/`>` input redirection
- Virtual environment is at `venv/` — activate before running or installing packages
