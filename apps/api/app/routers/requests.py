from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse, FileResponse
from typing import List
from .. import db, models, schemas
from sqlalchemy.orm import Session
from ..config import UPLOAD_DIR
from ..utils import save_upload_file
from ..celery_app import celery
from .. import tasks
import os

router = APIRouter()

# Dependency

def get_db():
    db_session = db.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


@router.post("/", response_model=schemas.RequestOut)
def create_request(payload: dict = None, db: Session = Depends(get_db)):
    req = models.Request(workspace_id=(payload.get('workspace_id') if payload else 1), status='PENDING')
    db.add(req)
    db.commit()
    db.refresh(req)
    return {"id": req.id, "status": req.status, "created_at": req.created_at.isoformat()}


@router.get("/", response_class=JSONResponse)
def list_requests(db: Session = Depends(get_db)):
    items = db.query(models.Request).order_by(models.Request.created_at.desc()).limit(100).all()
    return [{"id": r.id, "status": r.status, "created_at": r.created_at.isoformat()} for r in items]


@router.get("/{request_id}", response_model=schemas.RequestDetailOut)
def get_request(request_id: int, db: Session = Depends(get_db)):
    r = db.query(models.Request).filter_by(id=request_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Not found")
    fields = db.query(models.ExtractedField).filter_by(request_id=request_id).all()
    return {
        "id": r.id,
        "status": r.status,
        "extracted_fields": [
            {
                "id": f.id,
                "key": f.key,
                "value": f.value,
                "confidence": f.confidence,
                "source": f.source,
                "evidence_page": f.evidence_page,
                "evidence_text": f.evidence_text,
            }
            for f in fields
        ],
    }


@router.post("/{request_id}/upload-contract")
def upload_contract(request_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    r = db.query(models.Request).filter_by(id=request_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Request not found")
    # save file
    path = save_upload_file(file)
    # count pages naive: leave null for now or use pdfplumber later in task
    doc = models.Document(request_id=request_id, path=path, pages=None)
    db.add(doc)
    r.status = 'PENDING'
    db.commit()
    db.refresh(doc)
    return {"detail": "uploaded", "document_id": doc.id}


@router.post("/{request_id}/run-extraction")
def run_extraction(request_id: int, db: Session = Depends(get_db)):
    r = db.query(models.Request).filter_by(id=request_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Request not found")
    # mark processing
    r.status = 'PROCESSING'
    db.commit()
    # enqueue celery task
    celery.send_task('app.tasks.run_extraction', args=(request_id,))
    return {"detail": "extraction enqueued"}


@router.patch("/{request_id}/fields/{field_id}")
def patch_field(request_id: int, field_id: int, payload: dict, db: Session = Depends(get_db)):
    f = db.query(models.ExtractedField).filter_by(id=field_id, request_id=request_id).first()
    if not f:
        raise HTTPException(status_code=404, detail='Field not found')
    before = f.value
    # update value and mark source human
    f.value = payload.get('value')
    f.source = 'human'
    db.add(f)
    # write audit log
    al = models.AuditLog(workspace_id=f.request_id, request_id=request_id, user_id=None, action='update_field', field_key=f.key, before=str(before), after=str(f.value))
    db.add(al)
    db.commit()
    return {"detail": "field updated"}


@router.post("/{request_id}/mark-ready")
def mark_ready(request_id: int, db: Session = Depends(get_db)):
    r = db.query(models.Request).filter_by(id=request_id).first()
    if not r:
        raise HTTPException(status_code=404, detail='Request not found')
    r.status = 'READY'
    db.commit()
    return {"detail": "marked ready"}


@router.get("/{request_id}/export")
def export_package(request_id: int, db: Session = Depends(get_db)):
    r = db.query(models.Request).filter_by(id=request_id).first()
    if not r:
        raise HTTPException(status_code=404, detail='Request not found')
    fields = db.query(models.ExtractedField).filter_by(request_id=request_id).all()
    package = {f.key: {"value": f.value, "confidence": f.confidence, "source": f.source, "evidence_page": f.evidence_page, "evidence_text": f.evidence_text} for f in fields}
    return {"id": request_id, "package": package}
