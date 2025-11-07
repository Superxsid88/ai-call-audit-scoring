import os, json, asyncio
from typing import Dict, Any
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

HF_MODEL = os.getenv("ENGINE_HF_MODEL", "google/flan-t5-small")

# Lazy load to speed cold start
_tokenizer = None
_model = None
_pipe = None

def _ensure_pipe():
    global _tokenizer, _model, _pipe
    if _pipe is None:
        _tokenizer = AutoTokenizer.from_pretrained(HF_MODEL)
        _model = AutoModelForSeq2SeqLM.from_pretrained(HF_MODEL)
        _pipe = pipeline("text2text-generation", model=_model, tokenizer=_tokenizer)
    return _pipe

PROMPT = """You are a strict JSON scorer.
Read the call transcript and output ONLY valid JSON with keys:
- scores: object with keys ["Call Opening and Purpose Of Call","Hold Protocol","Resolution & Next Steps"] values one of ["Yes","No","NA"]
- audit_meta: include engine="HF_LOCAL" and a short "reason".
Transcript:
{transcript}
JSON:"""

async def hf_score(payload: Dict[str, Any]) -> Dict[str, Any]:
    pipe = _ensure_pipe()
    prompt = PROMPT.format(transcript=payload.get("transcript",""))
    # flan-t5 is deterministic at low temperature; pipeline ignores temperature but we keep generation small
    out = pipe(prompt, max_new_tokens=128)[0]["generated_text"]
    # best-effort JSON extraction
    start = out.find("{")
    end = out.rfind("}")
    if start >= 0 and end > start:
        out = out[start:end+1]
    try:
        parsed = json.loads(out)
    except Exception:
        # fallback to a minimal structure
        parsed = {
            "scores": {
                "Call Opening and Purpose Of Call": "NA",
                "Hold Protocol": "NA",
                "Resolution & Next Steps": "NA"
            },
            "audit_meta": {"engine": "HF_LOCAL", "reason": "fallback JSON parse"}
        }
    parsed.setdefault("audit_meta", {})
    parsed["audit_meta"]["engine"] = "HF_LOCAL"
    parsed["call_id"] = payload.get("call_id")
    return parsed
