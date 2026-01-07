import os
import json
from typing import Dict, Any
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')


def _safe_json_parse(text: str):
    try:
        return json.loads(text)
    except Exception:
        # Try to extract JSON substring
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(text[start:end+1])
            except Exception:
                return None
        return None


def extract_structured(prompt: str, keys: Dict[str, Any]):
    """Call OpenAI to extract structured fields.

    Returns a dict mapping each key to {value, confidence, evidence: {page, text}}
    If OPENAI_API_KEY is not set, returns empty/defaults.
    """
    if not openai.api_key:
        return {k: {"value": None, "confidence": 0.0, "evidence": {"page": None, "text": ""}} for k in keys}

    # Instruct model to reply with pure JSON matching the schema
    system = "You are a precise data extraction assistant. Return only JSON matching the requested schema."
    user = (
        "Extract the following fields from the provided contract text. "
        "Return a JSON object where each key maps to an object: {\"value\": ..., \"confidence\": 0-1, \"evidence\": {\"page\": int or null, \"text\": snippet}}."
        "If a field cannot be found, set value to null and confidence to 0."
        "\nFields: " + ", ".join(keys)
        + "\n\nContract text follows. Return only valid JSON."
    )

    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user + "\n\n" + prompt}],
            temperature=0.0,
            max_tokens=1500,
        )
        text = resp.choices[0].message.content
        parsed = _safe_json_parse(text)
        if not parsed:
            # fallback: return defaults
            return {k: {"value": None, "confidence": 0.0, "evidence": {"page": None, "text": ""}} for k in keys}
        # Normalize results to expected shape
        out = {}
        for k in keys:
            v = parsed.get(k)
            if isinstance(v, dict):
                out[k] = {
                    "value": v.get('value'),
                    "confidence": float(v.get('confidence') or 0.0),
                    "evidence": v.get('evidence') or {"page": None, "text": ""},
                }
            else:
                out[k] = {"value": v, "confidence": 0.0, "evidence": {"page": None, "text": ""}}
        return out
    except Exception:
        return {k: {"value": None, "confidence": 0.0, "evidence": {"page": None, "text": ""}} for k in keys}
