from datetime import datetime
from fastapi import UploadFile, HTTPException, Depends
from sqlmodel import Session
from app.models.Document.DocumentModel import Document, DocumentCreate
from app.database.database import get_db
import os
import uuid



from fastapi import Form, File, UploadFile

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def guardar_documento(file, title, department_id, doc_type_id, uploaded_by, company_id, db):
    # generar nombre único
    unique_name = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    # guardar físicamente el archivo
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # guardar en BD
    new_doc = Document(
        title=title,
        department_id=department_id,
        doc_type_id=doc_type_id,
        uploaded_by=uploaded_by,
        company_id=company_id,
        original_filename=unique_name
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return new_doc


def get_documents_by_user(user_id: int, db: Session  = Depends(get_db)):
    return db.query(Document).filter(Document.uploaded_by == user_id).all()

def get_documents_by_id(document_id: int, db: Session  = Depends(get_db)):
    document = db.query(Document).filter(Document.uploaded_by == document_id).first()

    if not document:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    
    if document.uploaded_by != id:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver este documento")

    return document


def get_all_documents(db: Session  = Depends(get_db)):
    return db.query(Document).all()

def delete_document(document_id: int, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    
    db.delete(document)
    db.commit()
    
    return {"detail": "Documento eliminado correctamente"}