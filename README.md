# VEX-Modular-AI-Stack
VEX's modular AI stack build that will include back and frontend API behaviour, personality core injection, local and OpenRouter model switching, RAG and agentic pipelines and more.

## Installation
1. Clone this repository.
2. (Optional) Create a Python virtual environment.
3. Install dependencies if a `requirements.txt` file is present:
   ```bash
   pip install -r requirements.txt
   ```

## Running locally
Start the backend:
```bash
python main.py
```

If you have a frontend, start it in another terminal:
```bash
cd frontend
npm install
npm run dev
```

## Docker usage
A Docker setup is provided to run the backend and a Node-based frontend.

1. Copy `.env.example` to `.env` and update the values.
2. Place any model files in the `models` directory.
3. Build and start the stack:
   ```bash
   cd docker
   docker compose up
   ```

The compose file mounts the `models` directory and `.env.example` into the backend container. The backend listens on port 8000 and the frontend on port 3000.
