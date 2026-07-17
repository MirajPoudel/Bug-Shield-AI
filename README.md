# 🛡️ BugShield-AI

**BugShield-AI** is an AI-powered code review tool. Paste code, upload a file, or point it at a public GitHub file, and a four-agent AI pipeline analyzes it for bugs, security issues, performance problems, and style — running entirely on a **local, self-hosted LLM** via [Ollama](https://ollama.com), with no external API keys required.

![Status](https://img.shields.io/badge/status-active-brightgreen) ![Python](https://img.shields.io/badge/python-3.12-blue) ![Streamlit](https://img.shields.io/badge/UI-Streamlit-ff4b4b)

---

## ✨ Features

- **Multi-agent AI review pipeline** — four specialized agents run in sequence:
  1. **Code Analyzer** — overall structure, quality summary, and score
  2. **Bug Detector** — bugs, security issues, and performance problems, with severity ratings
  3. **Improvement Agent** — concrete refactoring and best-practice suggestions
  4. **Doc Generator** — generates documentation for the submitted code
- **Three ways to submit code**: paste directly, upload a file, or fetch a file straight from a GitHub URL
- **Multiple local models** — switch between Qwen2.5-Coder, DeepSeek-Coder, CodeLlama, and Llama3 (auto-pulled via Ollama on first use)
- **19+ language support**, including Python, JavaScript/TypeScript, Java, Go, Rust, C/C++/C#, Ruby, PHP, Swift, Kotlin, Scala, and more (with auto-detection)
- **Score & results dashboard** — a review score, bug list, strengths, improvement suggestions, generated docs, and code view in a tabbed results page
- **Review history** — past reviews are saved per user and filterable by language
- **Simple built-in auth** — username/password sign-in and sign-up, no external identity provider needed
- **Runs fully offline** — the AI pipeline talks to a local Ollama server; no code you review is sent to a third-party API

---

## 🧱 Tech Stack

| Layer | Technology |
|---|---|
| UI | [Streamlit](https://streamlit.io) |
| AI orchestration | [LangGraph](https://www.langchain.com/langgraph) + [LangChain](https://www.langchain.com) |
| LLM runtime | [Ollama](https://ollama.com) (local, CPU-friendly models) |
| Auth & storage | Flat JSON files (no database) |
| Language | Python 3.12 |

> There is also an unused React/Vite + shadcn/ui scaffold under `artifacts/bugshield-ai/src/`. It is **not wired up** to the app below and can be ignored or removed — see the open follow-up task if you want to decide its fate.

---

## 📂 Project Structure

```
bugshield/
├── app.py                    # Streamlit entry point & page router
├── auth.py                   # JSON-file-based auth + review history storage
├── styles.py                 # Injected CSS for the dark UI theme
├── start.sh                  # Starts Ollama (if not running) then Streamlit
├── ollama_startup.sh         # Standalone helper to pre-pull the default model
├── .streamlit/
│   └── config.toml           # Streamlit server config (host, CORS, etc.)
├── agents/
│   ├── __init__.py
│   └── graph.py              # LangGraph pipeline: 4 agents + Ollama model management
├── pages/
│   ├── __init__.py
│   ├── landing.py            # Marketing landing page
│   ├── login.py              # Sign in / sign up
│   ├── review.py             # Code input (paste / upload / GitHub) + run pipeline
│   ├── results.py            # Score, bugs, strengths, improvements, docs, code tabs
│   └── history.py            # Past reviews, filterable by language
├── utils/
│   ├── __init__.py
│   └── github_fetcher.py     # Fetches & language-detects files from GitHub URLs
└── data/
    ├── users.json             # Seeded demo accounts + signups
    └── reviews.json           # Saved review history

question.md       # all the basic question of the system with their answer.
README.md       # all the information and command to run the system
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12
- [Ollama](https://ollama.com) installed and available on `PATH`

---

### ▶ Running on Replit
The Replit workflow (`artifacts/bugshield-ai: web`) runs `start.sh` automatically — no setup needed. The app becomes available on port `8501`.

---

### 🐧 Running on Linux
Install dependencies, then run the startup script:

```bash
pip install streamlit langgraph langchain-ollama requests
bash bugshield/start.sh
```

`start.sh` will start the Ollama server if it isn't already running, pull the default model, and then launch Streamlit.

---

### 🍎 Running on Mac
On Mac, Ollama runs as a background menu-bar app rather than a CLI server.

1. **Install Ollama** — download the Mac app from [ollama.com](https://ollama.com) and open it. It starts automatically and runs in the background.
2. **Install Python dependencies:**
   ```bash
   pip install streamlit langgraph langchain-ollama requests
   ```
3. **Pull the default model** (first time only):
   ```bash
   ollama pull qwen2.5-coder:1.5b
   ```
4. **Launch the app** — since Ollama is already running, skip `start.sh` and run Streamlit directly:
   ```bash
   streamlit run bugshield/app.py --server.port 8501
   ```
   Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

### First run
- `start.sh` automatically pulls the default model (`qwen2.5-coder:1.5b`, ~1 GB) **at startup** before Streamlit launches — so the very first review is instant with no waiting. On a cold container this takes ~30 seconds.
- A demo account is seeded automatically: **username** `demo`, **password** `demo123`.

---

## 🔍 How a Review Works

1. You submit code via the **Review** page (paste, file upload, or GitHub URL).
2. The pipeline (`agents/graph.py`) runs your code through four LangGraph nodes in sequence, each prompting the selected Ollama model:
   `Code Analyzer → Bug Detector → Improvement Agent → Doc Generator`
3. Each agent returns structured JSON (score, bug list, improvement list, or docs).
4. Results are saved to your review history and rendered on the **Results** page with a score, tabbed breakdown (bugs / strengths / improvements / docs / code), and metrics.

If a model call fails, the pipeline falls back to safe mock data so the UI never crashes on an unavailable model.

---

## 🧩 Available Models

| Model | Notes |
|---|---|
| `qwen2.5-coder:1.5b` | Default — fast, auto-installed |
| `qwen2.5-coder:7b` | Higher quality, slower |
| `deepseek-coder:1.3b` | Fast |
| `deepseek-coder:6.7b` | Higher quality |
| `codellama` | General code model |
| `llama3` | General-purpose |

Models are pulled on demand the first time they're selected; larger models take longer to download and run slower on CPU-only environments.

---

## 🗒️ Notes

- Auth and review history use flat JSON files (`bugshield/data/`) rather than a database — fine for a demo/small deployment, but not safe under concurrent writes at scale.
- The unused React scaffold in `artifacts/bugshield-ai/` is unrelated to the running app.
