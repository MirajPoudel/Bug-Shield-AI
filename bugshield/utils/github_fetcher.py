"""Fetch code from GitHub repositories."""
import re
import requests

def _detect_language(filename: str) -> str:
    ext_map = {
        ".py": "python", ".js": "javascript", ".ts": "typescript",
        ".jsx": "javascript", ".tsx": "typescript", ".java": "java",
        ".cpp": "cpp", ".c": "c", ".cs": "csharp", ".go": "go",
        ".rs": "rust", ".rb": "ruby", ".php": "php", ".swift": "swift",
        ".kt": "kotlin", ".scala": "scala", ".html": "html", ".css": "css",
        ".sh": "bash", ".sql": "sql", ".r": "r", ".m": "matlab"
    }
    for ext, lang in ext_map.items():
        if filename.lower().endswith(ext):
            return lang
    return "text"


def fetch_github_file(url: str) -> tuple[str, str, str]:
    """
    Fetch a single file from GitHub.
    Accepts:
    - https://github.com/user/repo/blob/branch/path/to/file
    - https://raw.githubusercontent.com/user/repo/branch/path/to/file
    Returns: (code, language, filename)
    """
    # Convert blob URL to raw
    raw_url = url
    if "github.com" in url and "/blob/" in url:
        raw_url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")

    response = requests.get(raw_url, timeout=15)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch file (HTTP {response.status_code}). Check the URL.")

    code = response.text
    filename = raw_url.split("/")[-1]
    language = _detect_language(filename)
    return code, language, filename


def fetch_github_repo_files(repo_url: str, max_files: int = 5) -> list[dict]:
    """
    Fetch main code files from a GitHub repo using the GitHub API.
    Returns list of {filename, code, language}
    """
    # Extract owner/repo
    match = re.search(r"github\.com/([^/]+)/([^/?\s]+)", repo_url)
    if not match:
        raise ValueError("Invalid GitHub repository URL.")

    owner, repo = match.group(1), match.group(2).rstrip(".git")

    # Get repo tree
    api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"
    resp = requests.get(api_url, timeout=15, headers={"Accept": "application/vnd.github.v3+json"})

    if resp.status_code == 404:
        raise ValueError(f"Repository '{owner}/{repo}' not found or is private.")
    if resp.status_code != 200:
        raise ValueError(f"GitHub API error: HTTP {resp.status_code}")

    tree = resp.json().get("tree", [])

    # Filter to code files, skip large files and non-code
    code_extensions = {".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".go", ".rs",
                       ".cpp", ".c", ".cs", ".rb", ".php", ".swift", ".kt"}
    skip_dirs = {"node_modules", "dist", "build", ".git", "__pycache__", "venv", ".venv"}

    code_files = []
    for item in tree:
        if item["type"] != "blob":
            continue
        path = item["path"]
        # Skip unwanted dirs
        parts = path.split("/")
        if any(p in skip_dirs for p in parts):
            continue
        ext = "." + path.rsplit(".", 1)[-1] if "." in path else ""
        if ext.lower() not in code_extensions:
            continue
        # Skip very large files
        if item.get("size", 0) > 50000:
            continue
        code_files.append({"path": path, "url": item.get("url", ""), "size": item.get("size", 0)})

    if not code_files:
        raise ValueError("No supported code files found in this repository.")

    # Pick the most interesting files (prioritize smaller files, main files)
    priority_names = {"main", "app", "index", "core", "utils", "helper", "api", "server", "model"}
    def score_file(f):
        name = f["path"].rsplit("/", 1)[-1].rsplit(".", 1)[0].lower()
        depth = f["path"].count("/")
        priority = -1 if name in priority_names else 0
        return (priority, depth, f["size"])

    code_files.sort(key=score_file)
    selected = code_files[:max_files]

    # Fetch raw content
    results = []
    base_raw = f"https://raw.githubusercontent.com/{owner}/{repo}/HEAD/"
    for f in selected:
        try:
            raw = requests.get(base_raw + f["path"], timeout=10)
            if raw.status_code == 200:
                lang = _detect_language(f["path"])
                results.append({
                    "filename": f["path"],
                    "code": raw.text,
                    "language": lang
                })
        except Exception:
            continue

    if not results:
        raise ValueError("Could not fetch any files from the repository.")

    return results


def detect_language_from_code(code: str) -> str:
    """Heuristic language detection from code content."""
    if re.search(r"^\s*import\s+\w+|from\s+\w+\s+import|def\s+\w+\s*\(|print\s*\(", code, re.MULTILINE):
        return "python"
    if re.search(r"function\s+\w+\s*\(|const\s+\w+\s*=|let\s+\w+|var\s+\w+|=>\s*{", code):
        return "javascript"
    if re.search(r"public\s+class|void\s+main|System\.out\.print", code):
        return "java"
    if re.search(r"#include\s*<|int\s+main\s*\(", code):
        return "cpp"
    if re.search(r"func\s+\w+\s*\(|:=|package\s+main", code):
        return "go"
    if re.search(r"fn\s+\w+\s*\(|let\s+mut|println!", code):
        return "rust"
    return "text"
