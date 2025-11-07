import asyncio
from typing import Dict, Any

RUBRIC = {
    "Call Opening and Purpose Of Call": ["hello", "welcome", "support", "how can i help"],
    "Hold Protocol": ["hold", "please wait", "one moment"],
    "Resolution & Next Steps": ["updated", "resolved", "anything else", "ticket"],
}

async def rule_score(payload: Dict[str, Any]) -> Dict[str, Any]:
    text = payload.get("transcript", "").lower()
    def has_any(keywords):
        return any(k in text for k in keywords)

    scores = {
        "Call Opening and Purpose Of Call": "Yes" if has_any(RUBRIC["Call Opening and Purpose Of Call"]) else "No",
        "Hold Protocol": "Yes" if has_any(RUBRIC["Hold Protocol"]) else "No",
        "Resolution & Next Steps": "Yes" if has_any(RUBRIC["Resolution & Next Steps"]) else "No",
    }
    audit_meta = {
        "engine": "RULE_BASED",
        "lang": payload.get("lang", "en"),
        "confidence_hint": 0.65 if "yes" in " ".join(scores.values()).lower() else 0.4,
    }
    await asyncio.sleep(0)
    return {"call_id": payload.get("call_id"), "scores": scores, "audit_meta": audit_meta}
