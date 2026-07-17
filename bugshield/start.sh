#!/usr/bin/env bash
cd "$(dirname "$0")"

if ! curl -sf http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "🦙 Starting Ollama server..."
    OLLAMA_HOST=0.0.0.0:11434 nohup ollama serve > /tmp/ollama.log 2>&1 &
    for i in $(seq 1 20); do
        curl -sf http://localhost:11434/api/tags > /dev/null 2>&1 && break
        sleep 1
    done
fi

MODEL="qwen2.5-coder:1.5b"
if ! curl -sf http://localhost:11434/api/tags | grep -q "$MODEL"; then
    echo "⬇️  Pulling $MODEL..."
    OLLAMA_HOST=0.0.0.0:11434 ollama pull "$MODEL"
fi

exec streamlit run app.py --server.port 8501 --server.address 0.0.0.0