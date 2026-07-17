# BugShield-AI

## Overview
BugShield-AI is a Streamlit web app that reviews source code using a local, multi-agent AI pipeline. Users paste code (or pull a file from a public GitHub URL), and a LangGraph pipeline of four agents — Code Analyzer, Bug Detector, Improvement Agent, and Doc Generator — runs against a locally hosted Ollama LLM to produce a score, bug list, improvement suggestions, and generated docs.

Auth is a simple JSON-file-based username/password system (see `bugshield/auth.py`), storing users and review history in `bugshield/data/`. There is no external database.

## Stack
- **App**: Python + Streamlit (`bugshield/app.py`, `bugshield/pages/`)
- **AI pipeline**: LangGraph + LangChain (`bugshield/agents/graph.py`), calling a local **Ollama** server (model: `qwen2.5-coder:1.5b`)
- **Storage**: flat JSON files in `bugshield/data/` (no database)

There is also an unrelated, unused React/Vite scaffold at `artifacts/bugshield-ai/src/` — it is not wired to the Streamlit app and can be ignored/removed later if not needed.

## Running the app
The app runs via the `artifacts/bugshield-ai: web` workflow, which executes `bugshield/start.sh`. That script:
1. Starts the local Ollama server in the background (`ollama serve`) if it isn't already running.
2. Launches Streamlit (`streamlit run app.py --server.port 8501 --server.address 0.0.0.0`).

The Ollama model (`qwen2.5-coder:1.5b`, ~1 GB) is pulled on demand the first time a review is run (see `ensure_model()` in `bugshield/agents/graph.py`); the first review after a fresh environment will be slower while it downloads.

Demo login credentials (seeded automatically in `bugshield/data/users.json` on first run):
- username `demo`, password `demo123`

## User preferences
None recorded yet.
