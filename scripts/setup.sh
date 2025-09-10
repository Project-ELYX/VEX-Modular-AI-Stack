#!/usr/bin/env bash
set -e

# Determine repository root
REPO_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/.. && pwd )"
cd "$REPO_ROOT"

# Install Python backend dependencies
pip install -r backend/requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd "$REPO_ROOT"

# Configure environment file
ENV_FILE="$REPO_ROOT/.env"
if [ ! -f "$ENV_FILE" ]; then
    cp .env.example "$ENV_FILE"
fi

read -p "Enter OpenRouter API key: " openrouter_key
read -p "Enter Anthropic API key: " anthropic_key
read -p "Enter local model path: " model_path
read -p "Use GPU? (true/false): " use_gpu

sed -i "s|OPENROUTER_API_KEY=.*|OPENROUTER_API_KEY=$openrouter_key|" "$ENV_FILE"
sed -i "s|ANTHROPIC_API_KEY=.*|ANTHROPIC_API_KEY=$anthropic_key|" "$ENV_FILE"
sed -i "s|LOCAL_MODEL_PATH=.*|LOCAL_MODEL_PATH=$model_path|" "$ENV_FILE"
sed -i "s|USE_GPU=.*|USE_GPU=$use_gpu|" "$ENV_FILE"

echo ".env configured at $ENV_FILE"

read -p "Start backend server now? (y/n): " start_backend
if [[ $start_backend == [yY]* ]]; then
    uvicorn backend.main:app --reload &
    BACKEND_PID=$!
fi

read -p "Start frontend dev server now? (y/n): " start_frontend
if [[ $start_frontend == [yY]* ]]; then
    cd frontend
    npm run dev &
    FRONTEND_PID=$!
    cd "$REPO_ROOT"
fi

if [[ -n "$BACKEND_PID" || -n "$FRONTEND_PID" ]]; then
    echo "Servers are running. Press Ctrl+C to stop."
    wait
fi
