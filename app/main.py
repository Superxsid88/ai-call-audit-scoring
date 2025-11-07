from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from app.services.scoring_engine import score_call

app = FastAPI(title="AI Call Audit Scoring", version="0.1.0")

class ScoreRequest(BaseModel):
    call_id: str = Field(..., description="Unique call identifier")
    transcript: str = Field(..., description="Raw transcript or diarized text")
    lang: str = "en"

@app.post("/score")
async def score(req: ScoreRequest):
    try:
        result = await score_call(req.model_dump())
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "ok"}
