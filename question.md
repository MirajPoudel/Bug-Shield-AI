# BugShield-AI — AI Architecture & File Guide

This document explains **how the AI side of BugShield-AI actually works** — the LLM, the agents, LangGraph, and (spoiler: there isn't one) RAG — plus what every file in the project does.

---

## 1. Quick answer: does it use RAG?

**No.** There is no retrieval-augmented generation anywhere in this codebase — no vector database, no embeddings, no document/chunk retrieval step. I searched the code for anything RAG-related (`embed`, `vector`, `retriev`, `faiss`, `chroma`, `pinecone`) and found nothing.

What it *does* do is closer to **direct prompting + multi-agent orchestration**: your submitted code is dropped straight into a series of prompt templates and sent to a local LLM, one agent at a time, with no retrieval or external knowledge lookup involved. If you want RAG-style behavior later (e.g. "review this code against our team's style guide" or "check against known CVE patterns"), that would need to be added — happy to help with that as a separate feature.

---

## 2. The LLM

- **Runtime**: [Ollama](https://ollama.com), running as a local server (`http://localhost:11434`) — not a cloud API. No API key is required, and code you submit never leaves the machine running the app.
- **Default model**: `qwen2.5-coder:1.5b` — a small, fast, code-tuned model that gets auto-downloaded (~1 GB) the first time you run a review, via `ensure_model()` in `bugshield/agents/graph.py`.
- **Model choice is user-selectable** on the Review page (`bugshield/pages/review.py`), from a fixed list:

  | Menu label | Ollama model tag |
  |---|---|
  | Qwen2.5-Coder 1.5B ⚡ (Fast) | `qwen2.5-coder:1.5b` |
  | Qwen2.5-Coder 7B (Better quality) | `qwen2.5-coder:7b` |
  | DeepSeek-Coder 1.3B ⚡ (Fast) | `deepseek-coder:1.3b` |
  | DeepSeek-Coder 6.7B | `deepseek-coder:6.7b` |
  | CodeLlama 7B | `codellama` |
  | Llama3 (General) | `llama3` |

  Switching models just changes which tag gets passed to `ChatOllama(model=...)` — any model not yet pulled locally is downloaded on first use.
- **LangChain integration**: `langchain_ollama.ChatOllama` is the client class that talks to the Ollama server and wraps responses in LangChain's message format. Temperature is kept low (`0.1`) for analysis/bugs/improvements (favors consistency), and slightly higher (`0.3`) for documentation generation (favors natural phrasing).

---

## 3. The AI agents (what "multi-agent" means here)

"Agent" in this project means **a single-purpose prompt + parsing step**, not an autonomous agent with tools or memory. There are four, and they always run in the same fixed order — there's no branching, looping, or agent-to-agent negotiation:

```
Code Analyzer → Bug Detector → Improvement Agent → Doc Generator
```

| Agent | File / function | What it asks the LLM for |
|---|---|---|
| **Code Analyzer** | `agents/graph.py` → `code_analyzer_node()` | Overall quality summary, a 0–100 score, a rating, and sub-scores for readability / maintainability / best practices, plus a list of strengths. |
| **Bug Detector** | `agents/graph.py` → `bug_detector_node()` | A list of bugs, security issues, and performance problems, each with a type, severity, description, and suggested fix. |
| **Improvement Agent** | `agents/graph.py` → `improvement_agent_node()` | Up to 5 concrete refactoring suggestions, each with a before/after code snippet. |
| **Doc Generator** | `agents/graph.py` → `doc_generator_node()` | Markdown documentation for the submitted code (description, params/returns, usage example, notes). |

Each node:
1. Builds a prompt asking the model to respond with a specific JSON shape (or markdown, for docs).
2. Calls the LLM via `_get_llm(model).invoke(prompt)`.
3. Parses the response with `_parse_json_response()`, which strips markdown code fences and tries to extract valid JSON even if the model wraps it in extra text.
4. **Falls back to hardcoded mock data** (`_mock_analysis()`, `_mock_bugs()`, `_mock_improvements()`, `_mock_docs()`) if the call fails or returns unparsable output — this is why the UI never crashes even if Ollama is down or the model returns garbage. It's worth knowing this fallback exists: if results look suspiciously generic, it likely means the real model call failed silently.

Agents don't share reasoning with each other — each one only sees the original code, language, and model choice. The only thing that flows agent-to-agent is the accumulating `ReviewState` dictionary (see below), so agent 4 doesn't "know" what agent 2 found unless you extend the prompts to pass that along.

---

## 4. LangGraph — how the agents are wired together

[LangGraph](https://www.langchain.com/langgraph) is used purely as an **orchestration/state-machine layer** on top of the four agent functions — think of it as a typed pipeline runner, not a decision-making agent framework here.

In `agents/graph.py`:

- **`ReviewState`** (a `TypedDict`) defines the shared state object passed through the whole pipeline: `code`, `language`, `model`, plus each agent's output field (`analysis`, `bugs`, `improvements`, `docs`, `score`, `summary`, `error`).
- **`build_review_graph()`** constructs a `StateGraph(ReviewState)`, registers the four node functions, and wires them with a straight line of edges:
  ```
  code_analyzer → bug_detector → improvement_agent → doc_generator → END
  ```
  There are no conditional edges, no cycles, and no retries at the graph level — it's a linear pipeline. LangGraph's value here is mainly a clean, typed way to compose the steps and merge each node's returned state into the whole.
- **`run_review(code, language, model)`** is the entry point used by the UI (`pages/review.py`). It:
  1. Calls `ensure_model(model)` to make sure the chosen model is pulled locally (pulls it via `ollama pull` if missing).
  2. Builds and compiles the graph.
  3. Invokes it with an initial state built from your submitted code.
  4. Returns the final state dict, which the Results page renders.

---

## 5. Data flow, end to end

```
┌─────────────┐     ┌───────────────┐     ┌────────────────────────┐     ┌──────────────┐
│ Review page │ ──▶ │ run_review()  │ ──▶ │ LangGraph pipeline      │ ──▶ │ Results page │
│ (your code) │     │ agents/graph.py│     │ 4 agents → Ollama LLM   │     │ (score, bugs,│
└─────────────┘     └───────────────┘     └────────────────────────┘     │ improvements, │
                                                                          │  docs, code)  │
                                                                          └──────┬────────┘
                                                                                 │
                                                                                 ▼
                                                                    auth.save_review() →
                                                                    bugshield/data/reviews.json
```

No step here fetches outside context to feed the model (no RAG); the only "external" input source is the GitHub fetcher, which just retrieves raw code text to review — it does not feed the model anything beyond that code.

---

## 6. File-by-file guide

### App shell
- **`bugshield/app.py`** — Streamlit entry point. Sets page config, initializes session state (login status, current page, review result, selected model), and routes to the right page module based on `st.session_state.page`.
- **`bugshield/styles.py`** — Injects the app's custom dark-theme CSS (no AI logic; pure presentation).
- **`bugshield/start.sh`** — Startup script used by the Replit workflow: starts the local Ollama server in the background if it isn't already running, then launches Streamlit.
- **`bugshield/ollama_startup.sh`** — Standalone helper that waits for Ollama to come up and pre-pulls the default model; not called automatically by the app (models are pulled lazily via `ensure_model()` instead), but handy for warming the cache ahead of time.

### Auth & storage
- **`bugshield/auth.py`** — All persistence logic. Seeds two demo accounts on first run, hashes passwords (SHA-256), and reads/writes:
  - `bugshield/data/users.json` — user accounts
  - `bugshield/data/reviews.json` — saved review history, keyed by username
  Also exposes `login()`, `signup()`, and `save_review()` used by the pages.

### AI pipeline
- **`bugshield/agents/graph.py`** — Everything described in sections 2–4 above: the LLM client, the four agent node functions, the LangGraph pipeline definition, and `run_review()`.
- **`bugshield/utils/github_fetcher.py`** — Not AI-related. Converts a GitHub `blob` URL to its raw-content URL, downloads the file over HTTP, and guesses its language from the file extension so it can be handed to the review pipeline like any pasted snippet.

### Pages (UI)
- **`bugshield/pages/landing.py`** — Marketing/landing page with hero section and sign-in button; no AI calls.
- **`bugshield/pages/login.py`** — Sign in / sign up forms, calling `auth.login()` / `auth.signup()`.
- **`bugshield/pages/review.py`** — The input page: three tabs (paste code / upload file / GitHub URL), language and model selectors, and the button that triggers `run_review()`. This is the only page that calls into the AI pipeline.
- **`bugshield/pages/results.py`** — Renders the pipeline output: score circle, tabs for bugs / strengths / improvements / docs / original code.
- **`bugshield/pages/history.py`** — Lists past reviews for the logged-in user, filterable by language, reading from `auth`'s stored review history.

### Unrelated / not integrated
- **`artifacts/bugshield-ai/`** — A separate React + Vite + shadcn/ui scaffold. It is **not connected** to the Streamlit app or the AI pipeline described above; it exists in the repo but isn't part of the running product.

---

## 7. Summary — the honest one-liner

BugShield-AI is a **linear, local, four-step LLM prompting pipeline** (Analyzer → Bug Detector → Improver → Doc Generator) orchestrated with **LangGraph**, running against a **local Ollama model** via **LangChain**, with graceful mock-data fallbacks — and **no RAG, no tool-using agents, and no external AI API calls**.
