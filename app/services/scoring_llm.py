import os, json, httpx
from typing import Dict, Any

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

PROMPT_TEMPLATE = """You are an auditing assistant. Read the call transcript and return a STRICT JSON with keys:
- scores: object with keys ["Call Opening and Purpose Of Call","Hold Protocol","Resolution & Next Steps"] values one of ["Yes","No","NA"]
- audit_meta: include engine="LLM", confidence (0-1), and 1-line reason.
Transcript:
{transcript}
Return ONLY JSON.
"""

async def llm_score(payload: Dict[str, Any]) -> Dict[str, Any]:
    if not OPENAI_API_KEY:
        raise RuntimeError("Set OPENAI_API_KEY to use ENGINE=LLM")

    prompt = PROMPT_TEMPLATE.format(transcript=payload.get("transcript", ""))

    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
            json={
                "model": OPENAI_MODEL,
                "temperature": 0.2,
                "messages": [
                    {"role": "system", "content": "Only output valid JSON. No extra text."},
                    {"role": "user", "content": prompt}
                ]
            }
        )
        resp.raise_for_status()
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
        try:
            parsed = json.loads(content)
        except Exception:
            start = content.find("{")
            end = content.rfind("}")
            parsed = json.loads(content[start:end+1])
    parsed.setdefault("audit_meta", {})
    parsed["audit_meta"].update({"engine": "LLM"})
    parsed["call_id"] = payload.get("call_id")
    return parsed
