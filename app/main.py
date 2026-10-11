from pathlib import Path
import json
import shutil

from fastapi import Depends, FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine, get_db
from app.models import Document
from app.schemas import DocumentResponse
from app.services.analysis_service import process_document


BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "data" / "uploads"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Compliance AI Project",
    description="AI-powered compliance document analysis system",
    version="1.0.0",
)

templates = Jinja2Templates(
    directory=str(BASE_DIR / "app" / "templates")
)

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "app" / "static")),
    name="static",
)


ALLOWED_EXTENSIONS = {
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".tiff",
    ".bmp",
}


@app.get("/", response_class=HTMLResponse)
def dashboard(
    request: Request,
    db: Session = Depends(get_db),
):
    documents = (
        db.query(Document)
        .order_by(Document.created_at.desc())
        .all()
    )

    total_documents = len(documents)
    high_priority = sum(1 for document in documents if document.priority == "High")
    medium_priority = sum(1 for document in documents if document.priority == "Medium")
    low_priority = sum(1 for document in documents if document.priority == "Low")

    deadlines = []
    checklist_overview = []

    for document in documents:
        dates = json.loads(document.compliance_dates or "[]")
        checklist = json.loads(document.checklist or "[]")

        checklist_overview.append({
            "filename": document.filename,
            "count": len(checklist),
            "priority": document.priority,
        })

        for date in dates:
            deadlines.append({
                "filename": document.filename,
                "date": date,
                "priority": document.priority,
            })

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "documents": documents,
            "total_documents": total_documents,
            "high_priority": high_priority,
            "medium_priority": medium_priority,
            "low_priority": low_priority,
            "deadlines": deadlines,
            "checklist_overview": checklist_overview,
        },
    )


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Compliance AI",
    }


@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No filename provided.",
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and image files are supported.",
        )

    safe_filename = Path(file.filename).name
    file_path = UPLOAD_DIR / safe_filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        result = process_document(str(file_path))
    except Exception as exc:
        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=f"Document processing failed: {exc}",
        ) from exc

    document = Document(
        filename=result["filename"],
        file_path=result["file_path"],
        language=result.get("language", "unknown"),
        document_type=result.get("document_type", "Other"),
        summary=result.get("summary", ""),
        important_clauses=json.dumps(
            result.get("important_clauses", []),
            ensure_ascii=False,
        ),
        compliance_dates=json.dumps(
            result.get("compliance_dates", []),
            ensure_ascii=False,
        ),
        checklist=json.dumps(
            result.get("checklist", []),
            ensure_ascii=False,
        ),
        priority=result.get("priority", "Medium"),
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return {
        "message": "Document uploaded and analyzed successfully.",
        "document_id": document.id,
        "filename": document.filename,
        "language": document.language,
        "document_type": document.document_type,
        "priority": document.priority,
    }


@app.get("/documents", response_model=list[DocumentResponse])
def get_documents(
    db: Session = Depends(get_db),
):
    return (
        db.query(Document)
        .order_by(Document.created_at.desc())
        .all()
    )


@app.get("/documents/{document_id}", response_class=HTMLResponse)
def document_detail(
    document_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    clauses = json.loads(document.important_clauses or "[]")
    dates = json.loads(document.compliance_dates or "[]")
    checklist = json.loads(document.checklist or "[]")

    return templates.TemplateResponse(
        request=request,
        name="document.html",
        context={
            "document": document,
            "clauses": clauses,
            "dates": dates,
            "checklist": checklist,
        },
    )


@app.delete("/documents/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
):
    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    file_path = Path(document.file_path)

    if file_path.exists():
        file_path.unlink()

    db.delete(document)
    db.commit()

    return {
        "message": "Document deleted successfully.",
        "document_id": document_id,
    }












