# VEX-Modular-AI-Stack
VEX's modular AI stack build that will include back and frontend API behaviour, personality core injection, local and OpenRouter model switching, RAG and agentic pipelines and more.

## Setup
1. Clone this repository.
2. (Optional) Create a Python virtual environment.
3. Copy `.env.example` to `.env` and update the values (e.g. set `VECTOR_BACKEND`
   to `chroma` or `qdrant`).
4. Place any model files in the `models` directory.

## Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn backend.main:app --reload  # run the backend API
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Docker Compose
```bash
cp .env.example .env
cd docker
docker compose up
```

The compose file mounts the `models` directory and `.env` into the backend container. The backend listens on port 8000 and the frontend on port 5173.
