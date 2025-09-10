from fastapi import UploadFile, HTTPException, Depends
from sqlmodel import Session
from app.models.Document.DocumentModel import Document, DocumentCreate
from app.database.database import get_db

def guardar_documento( file: UploadFile, doc_data: DocumentCreate, db: Session = Depends(get_db)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")

    doc = Document(
        department_id=doc_data.department_id,
        uploaded_by=doc_data.uploaded_by,
        doc_type_id=doc_data.doc_type_id,
        company_id=doc_data.company_id,
        title=doc_data.title,
        original_filename=file.filename,
        processed=0
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    return doc

def get_documents_by_user(user_id: int, db: Session  = Depends(get_db)):
    return db.query(Document).filter(Document.uploaded_by == user_id).all()

def get_documents_by_id(document_id: int, db: Session  = Depends(get_db)):
    document = db.query(Document).filter(Document.uploaded_by == document_id).first()

    if not document:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    
    if document.uploaded_by != id:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver este documento")

    return document

