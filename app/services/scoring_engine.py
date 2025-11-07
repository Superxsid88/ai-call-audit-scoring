import os, json, hashlib
from typing import Dict, Any
from app.utils.cache import maybe_get_cache, maybe_set_cache
from app.services.scoring_llm import llm_score
from app.services.scoring_rules import rule_score

ENGINE = os.getenv("ENGINE", "RULE_BASED").upper()
ENABLE_CACHE = os.getenv("ENABLE_CACHE", "false").lower() == "true"

def _cache_key(payload: Dict[str, Any]) -> str:
    return "score:" + hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

async def score_call(payload: Dict[str, Any]) -> Dict[str, Any]:
    key = _cache_key(payload)
    if ENABLE_CACHE:
        cached = await maybe_get_cache(key)
        if cached:
            return cached
    if ENGINE == "LLM":
        result = await llm_score(payload)
    else:
        result = await rule_score(payload)
    if ENABLE_CACHE:
        await maybe_set_cache(key, result, ttl=3600)
    return result
