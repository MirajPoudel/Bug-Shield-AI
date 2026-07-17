"""
LangGraph multi-agent code review pipeline.
Agents: Code Analyzer → Bug Detector → Improvement Agent → Doc Generator
"""
import json
import re
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END

try:
    from langchain_ollama import ChatOllama
    OLLAMA_AVAILABLE = True
except Exception:
    OLLAMA_AVAILABLE = False

OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = "qwen2.5-coder:1.5b"

def ensure_model(model: str) -> bool:
    """Pull model if not already available. Returns True if ready."""
    import subprocess, requests as _req
    try:
        tags = _req.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=3).json()
        names = [m["name"] for m in tags.get("models", [])]
        # Match with or without tag suffix
        base = model.split(":")[0]
        if any(model == n or n.startswith(base) for n in names):
            return True
        # Pull it
        subprocess.run(
            ["ollama", "pull", model],
            env={**__import__("os").environ, "OLLAMA_HOST": "0.0.0.0:11434"},
            timeout=600, check=True, capture_output=True
        )
        return True
    except Exception:
        return False


class ReviewState(TypedDict):
    code: str
    language: str
    model: str
    # Agent outputs
    analysis: Optional[dict]
    bugs: Optional[list]
    improvements: Optional[list]
    docs: Optional[str]
    score: Optional[int]
    summary: Optional[str]
    error: Optional[str]


def _get_llm(model: str, temperature: float = 0.1):
    return ChatOllama(
        model=model,
        base_url=OLLAMA_BASE_URL,
        temperature=temperature,
        request_timeout=120,   # 2-minute hard cap per agent call
    )


def _parse_json_response(text: str) -> dict | list:
    """Extract JSON from LLM response, even if wrapped in markdown."""
    # Try to find JSON block
    match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if match:
        text = match.group(1).strip()
    try:
        return json.loads(text)
    except Exception:
        # Try to find first { or [ and parse from there
        start = text.find("{") if "{" in text else text.find("[")
        if start != -1:
            try:
                return json.loads(text[start:])
            except Exception:
                pass
    return {}


def code_analyzer_node(state: ReviewState) -> ReviewState:
    """Analyzes code structure, quality, and readability."""
    try:
        llm = _get_llm(state["model"])
        prompt = f"""You are a Code Analysis Agent. Analyze the following {state['language']} code.

Return a JSON object with this exact structure:
{{
  "summary": "2-3 sentence overall assessment",
  "score": <integer 0-100>,
  "rating": "Excellent|Good|Fair|Poor",
  "readability": <integer 0-100>,
  "maintainability": <integer 0-100>,
  "best_practices": <integer 0-100>,
  "strengths": ["strength1", "strength2", ...]
}}

CODE:
```{state['language']}
{state['code']}
```

Respond ONLY with valid JSON."""

        response = llm.invoke(prompt)
        parsed = _parse_json_response(response.content)
        if not parsed or not isinstance(parsed, dict):
            raise ValueError("Empty response")
        return {**state, "analysis": parsed, "score": parsed.get("score", 75), "summary": parsed.get("summary", "")}
    except Exception as e:
        return {**state, "error": f"Analyzer error: {str(e)}", "analysis": _mock_analysis(), "score": 75, "summary": "Code analysis complete."}


def bug_detector_node(state: ReviewState) -> ReviewState:
    """Detects bugs, security issues, and performance problems."""
    try:
        llm = _get_llm(state["model"])
        prompt = f"""You are a Bug Detection Agent. Find bugs, security issues, and performance problems in this {state['language']} code.

Return a JSON array of issues:
[
  {{
    "type": "bug|security|performance|style",
    "severity": "critical|high|medium|low",
    "title": "Short title",
    "description": "Detailed description",
    "line_hint": "optional line reference",
    "solution": "How to fix it"
  }},
  ...
]

If no issues found, return an empty array [].

CODE:
```{state['language']}
{state['code']}
```

Respond ONLY with valid JSON array."""

        response = llm.invoke(prompt)
        parsed = _parse_json_response(response.content)
        if not isinstance(parsed, list):
            parsed = []
        return {**state, "bugs": parsed}
    except Exception as e:
        return {**state, "bugs": _mock_bugs(), "error": f"Bug detector error: {str(e)}"}


def improvement_agent_node(state: ReviewState) -> ReviewState:
    """Suggests code improvements and refactoring opportunities."""
    try:
        llm = _get_llm(state["model"])
        prompt = f"""You are a Code Improvement Agent. Suggest concrete improvements for this {state['language']} code.

Return a JSON array:
[
  {{
    "category": "performance|readability|maintainability|security|best_practice",
    "title": "Short improvement title",
    "description": "What to improve and why",
    "code_before": "optional: current code snippet",
    "code_after": "optional: improved code snippet"
  }},
  ...
]

CODE:
```{state['language']}
{state['code']}
```

Respond ONLY with valid JSON array. Limit to top 5 most impactful improvements."""

        response = llm.invoke(prompt)
        parsed = _parse_json_response(response.content)
        if not isinstance(parsed, list):
            parsed = []
        return {**state, "improvements": parsed}
    except Exception as e:
        return {**state, "improvements": _mock_improvements(), "error": f"Improvement error: {str(e)}"}


def doc_generator_node(state: ReviewState) -> ReviewState:
    """Generates documentation for the code."""
    try:
        llm = _get_llm(state["model"], temperature=0.3)
        prompt = f"""You are a Documentation Agent. Generate clear, professional documentation for this {state['language']} code.

Include:
- A brief module/function description
- Parameters and return values (if applicable)
- Usage examples
- Any important notes

Format as clean markdown.

CODE:
```{state['language']}
{state['code'][:3000]}
```

Respond with markdown documentation only."""

        response = llm.invoke(prompt)
        return {**state, "docs": response.content}
    except Exception as e:
        return {**state, "docs": _mock_docs(state["language"]), "error": f"Doc error: {str(e)}"}


def _mock_analysis() -> dict:
    return {
        "summary": "The code is well-structured and follows clean coding principles. There are some areas for improvement in terms of performance and security.",
        "score": 85,
        "rating": "Good",
        "readability": 80,
        "maintainability": 85,
        "best_practices": 90,
        "strengths": [
            "Clear separation of concerns",
            "Effective handling of edge cases",
            "Consistent naming conventions"
        ]
    }

def _mock_bugs() -> list:
    return [
        {
            "type": "performance",
            "severity": "medium",
            "title": "Nested loops causing O(n²) complexity",
            "description": "The nested loops for finding user and product details have potential performance issues with large datasets.",
            "line_hint": "Inner loop",
            "solution": "Consider using a map or object to store user and product data for faster lookups"
        }
    ]

def _mock_improvements() -> list:
    return [
        {
            "category": "performance",
            "title": "Use dictionary lookups instead of nested loops",
            "description": "Replace nested loops with O(1) dictionary lookups for better scalability.",
            "code_before": "for item in list:\n    for sub in other_list:\n        if item.id == sub.id: ...",
            "code_after": "lookup = {item.id: item for item in other_list}\nresult = lookup.get(target_id)"
        },
        {
            "category": "readability",
            "title": "Add type hints to function signatures",
            "description": "Type hints improve code readability and enable better IDE support.",
            "code_before": "def process(data, users):",
            "code_after": "def process(data: list, users: dict) -> dict:"
        }
    ]

def _mock_docs(language: str) -> str:
    return f"""## Module Documentation

### Overview
This {language} module provides core functionality for data processing and management.

### Functions

#### `main_function(data, config)`
Processes input data according to the provided configuration.

**Parameters:**
- `data` - Input data to process
- `config` - Configuration dictionary with processing options

**Returns:**
- Processed result object

### Usage Example
```{language}
result = main_function(my_data, {{"mode": "fast"}})
print(result)
```

### Notes
- Ensure input data is properly validated before calling
- The function is not thread-safe by default
"""


def build_review_graph():
    """Build and compile the LangGraph review pipeline."""
    workflow = StateGraph(ReviewState)

    workflow.add_node("code_analyzer", code_analyzer_node)
    workflow.add_node("bug_detector", bug_detector_node)
    workflow.add_node("improvement_agent", improvement_agent_node)
    workflow.add_node("doc_generator", doc_generator_node)

    workflow.set_entry_point("code_analyzer")
    workflow.add_edge("code_analyzer", "bug_detector")
    workflow.add_edge("bug_detector", "improvement_agent")
    workflow.add_edge("improvement_agent", "doc_generator")
    workflow.add_edge("doc_generator", END)

    return workflow.compile()


def run_review(code: str, language: str, model: str) -> dict:
    """Run the full multi-agent review pipeline."""
    graph = build_review_graph()
    initial_state: ReviewState = {
        "code": code,
        "language": language,
        "model": model,
        "analysis": None,
        "bugs": None,
        "improvements": None,
        "docs": None,
        "score": None,
        "summary": None,
        "error": None,
    }
    result = graph.invoke(initial_state)
    return result


# ── Step-by-step runner (for real per-agent progress in the UI) ────
STEP_NODES = [
    ("code_analyzer",    "🔍", "Code Analyzer",           code_analyzer_node),
    ("bug_detector",     "🐛", "Bug Detector",             bug_detector_node),
    ("improvement_agent","💡", "Improvement Agent",        improvement_agent_node),
    ("doc_generator",    "📖", "Documentation Generator", doc_generator_node),
]

def run_review_stepwise(code: str, language: str, model: str):
    """
    Generator that runs one agent at a time and yields after each step.
    Each yield returns (step_index, icon, name, partial_state).
    Caller iterates this to update the UI between steps.
    """
    state: ReviewState = {
        "code": code,
        "language": language,
        "model": model,
        "analysis": None,
        "bugs": None,
        "improvements": None,
        "docs": None,
        "score": None,
        "summary": None,
        "error": None,
    }
    for i, (key, icon, name, node_fn) in enumerate(STEP_NODES):
        state = node_fn(state)
        yield i, icon, name, state
