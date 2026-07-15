#!/usr/bin/env bash
# Auto-pull the default model if not already present.
# Called once at BugShield startup.

MODEL="qwen2.5-coder:1.5b"
OLLAMA_HOST="http://localhost:11434"

echo "🛡️  BugShield-AI — checking Ollama model..."

# Wait up to 30 s for Ollama to be ready
for i in $(seq 1 30); do
    if curl -sf "$OLLAMA_HOST/api/tags" > /dev/null 2>&1; then
        break
    fi
    sleep 1
done

# Check if model is already pulled
if curl -sf "$OLLAMA_HOST/api/tags" | grep -q "$MODEL"; then
    echo "✅  Model '$MODEL' already available."
else
    echo "⬇️   Pulling '$MODEL' (first time only, ~1 GB)..."
    OLLAMA_HOST=0.0.0.0:11434 ollama pull "$MODEL"
    echo "✅  Model ready."
fi
