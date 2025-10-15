# Demojifier Project

## Overview
Demojifier is a web application that converts text containing emojis into their English meanings using both rules-based heuristics and an LLM (Large Language Model) backend. The project consists of a Python FastAPI backend and a simple HTML/JavaScript frontend.

## Features
- Convert emojis in text to their English meanings
- Two modes: rules-only (offline) and LLM (online, with API key)
- Interactive web frontend
- REST API for programmatic access

## Project Structure
```
Warmup project/
├── backend/
│   ├── demojify_lib.py      # Core emoji conversion logic
│   ├── main.py              # FastAPI backend server
│   ├── llm_test_script.py   # Standalone test script
│   ├── requirements.txt     # Python dependencies
│   └── __pycache__/         # Python cache files
├── frontend/
│   └── index.html           # Web frontend
```

## Setup & Installation

### 1. Backend (API Server)
- Install Python 3.9+
- Install dependencies:
  ```
  pip install -r backend/requirements.txt
  ```
- Start the server:
  ```
  cd backend
  python main.py
  uvicorn main:app --reload --port 8000
  ```
- The API will run at `http://127.0.0.1:8000`

### 2. Frontend (Web App)
- Open `frontend/index.html` in your browser
- Or, after starting the backend, visit `http://127.0.0.1:8000/` (served by FastAPI)

## API Endpoints
- `POST /api/convert` — Convert emojis in text
- `GET /health` — Health check
- `GET /` or `/index` — Serves the frontend
- `GET /docs` — Interactive API docs (Swagger UI)

## Usage
- Paste text with emojis into the web app and click "Convert"
- Choose "rules only" for offline conversion, or "auto" for LLM + rules fallback
- The output will show the converted text and the source (llm or standard)

## Customization
- Emoji mappings and rules are in `demojify_lib.py`
- LLM integration requires an API key (see environment variable `OPENAI_API_KEY`)

## Testing
- Run `peter_colab.py` for standalone testing of the conversion logic

## License
MIT License

## Credits
- Built with FastAPI, Pydantic, and emoji Python package
- Frontend uses HTML/CSS/JS
