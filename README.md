# AI Call Audit Scoring (Cost-Efficient, Production-Ready Skeleton)

FastAPI-based **call audit scoring** service with:
- **LLM optional** (OpenAI/Gemini) — default is **offline rule-based** to keep costs near-zero.
- **Async API**, structured JSON responses, and testable modules.
- **Redis caching** (optional) and Docker deployment for local or **GCP Cloud Run**.
- Designed for low-cost hardware (**RTX 3050 4GB**) and **GCP credits**.

## ✨ Features
- POST `/score` → returns rubric-based audit scores from a raw transcript or diarized JSON.
- Two engines:
  1. `RULE_BASED` (default): deterministic, zero-cost, robust baseline.
  2. `LLM` (optional): uses OpenAI or Gemini; enable with env flags.
- Hallucination-safe: JSON schema validation and guardrails at prompt level.
- Minimal dependencies; runs on CPU/GPU.

## 🏗️ Architecture
```
FastAPI → Service (rule/LLM) → Post-process → JSON
                          ↘ Redis cache (optional)
```

## ⚙️ Quickstart (Local)
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
# Test
curl -X POST http://127.0.0.1:8000/score -H "Content-Type: application/json" -d @example_input.json
```

## 🔧 Env Configuration
Copy `.env.example` to `.env` and edit if needed:
```env
ENGINE=RULE_BASED            # RULE_BASED or LLM
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
REDIS_URL=redis://localhost:6379/0
ENABLE_CACHE=false
```

## 🐳 Docker
```bash
docker build -t ai-call-audit-scoring .
docker run -p 5002:5002 --env-file .env ai-call-audit-scoring
```

## ☁️ Deploy to GCP Cloud Run (Cheapest, Serverless)
```bash
gcloud builds submit --tag gcr.io/$PROJECT_ID/ai-call-audit-scoring
gcloud run deploy ai-call-audit-scoring --image gcr.io/$PROJECT_ID/ai-call-audit-scoring --platform managed --allow-unauthenticated --memory 512Mi --cpu 1 --max-instances=2
```
> Tip: Use `--max-instances=2` and request-based concurrency to control cost.

## 🧪 Tests
```bash
pytest -q
```

## 📄 Example Input
See `example_input.json`.

## 📦 Tech
FastAPI, Pydantic, (optional) Redis, (optional) OpenAI/Gemini.

## 📜 License
MIT
