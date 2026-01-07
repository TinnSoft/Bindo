import os
from .celery_app import celery
from .db import SessionLocal
from . import models
import pdfplumber
from .llm_client import extract_structured
import os

SCHEMA_KEYS = [
    'contract_object',
    'contract_value',
    'term_months',
    'advance_percentage',
    'contracting_entity'
]


@celery.task(name='app.tasks.run_extraction')
def run_extraction_task(request_id: int):
    db = SessionLocal()
    try:
        req = db.query(models.Request).filter_by(id=request_id).first()
        if not req:
            return {'error': 'request not found'}
        # find latest document
        doc = db.query(models.Document).filter_by(request_id=request_id).order_by(models.Document.uploaded_at.desc()).first()
        if not doc or not os.path.exists(doc.path):
            return {'error': 'document not found'}

        pages_text = []
        with pdfplumber.open(doc.path) as pdf:
            for i, p in enumerate(pdf.pages, start=1):
                text = p.extract_text() or ''
                pages_text.append({'page': i, 'text': text})
        # update doc.pages
        try:
            doc.pages = len(pages_text)
            db.add(doc)
            db.commit()
        except Exception:
            db.rollback()

        # Build a concise prompt: include numbered page snippets (truncate long pages)
        snippets = []
        for p in pages_text:
            snippet = (p['text'][:1500] + '...') if len(p['text']) > 1500 else p['text']
            snippets.append(f"[PAGE {p['page']}]: {snippet}")

        prompt = "\n\n".join(snippets)
        # Call LLM to extract structured data
        result = extract_structured(prompt, SCHEMA_KEYS)

        # Persist extracted fields, replace existing for the request
        # delete old LLM fields for this request to avoid duplicates
        db.query(models.ExtractedField).filter_by(request_id=request_id, source='llm').delete()
        db.commit()

        for key, data in result.items():
            value = data.get('value')
            confidence = float(data.get('confidence') or 0.0)
            evidence = data.get('evidence') or {}
            ef = models.ExtractedField(
                request_id=request_id,
                key=key,
                value=str(value) if value is not None else None,
                confidence=confidence,
                source='llm',
                evidence_page=(evidence.get('page') if evidence.get('page') is not None else None),
                evidence_text=(evidence.get('text') or '')
            )
            db.add(ef)

        req.status = 'REVIEW'
        db.commit()
        return {'status': 'ok'}
    finally:
        db.close()
