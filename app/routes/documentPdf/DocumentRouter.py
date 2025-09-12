from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlmodel import Session
from app.database.database import get_db
from app.controllers.documents.documentsController import guardar_documento, get_documents_by_user, get_documents_by_id, get_all_documents, delete_document
from app.models.Document.DocumentModel import DocumentCreate

router = APIRouter(tags=["Documents"])


@router.post("/")
async def upload_document(
    file: UploadFile = File(...),
    department_id: int = Form(...),
    uploaded_by: int = Form(...),
    doc_type_id: int = Form(...),
    company_id: int = Form(...),
    title: str = Form(...),
    db: Session = Depends(get_db)
):
    doc_data = DocumentCreate(
        department_id=department_id,
        uploaded_by=uploaded_by,
        doc_type_id=doc_type_id,
        company_id=company_id,
        title=title
    )

    doc = guardar_documento(file=file, doc_data=doc_data, db=db)

    return {"message": "Documento guardado correctamente", "document": doc}

@router.get("/user/{user_id}")
def read_documents_by_user(user_id: int, db: Session = Depends(get_db)):
    documents = get_documents_by_user(user_id=user_id, db=db)
    return {"documento": documents}

@router.get("/{document_id}")
def read_document_by_id(document_id: int, db: Session = Depends(get_db)):
    document = get_documents_by_id(document_id=document_id, db=db)
    return {"documento": document}

@router.get("/")
def read_all_documents(db: Session = Depends(get_db)):
    documents = get_all_documents(db=db)
    return {"documents": documents}

@router.delete("/{document_id}")
def delete_document_route(document_id: int, db: Session = Depends(get_db)):
    result = delete_document(document_id=document_id, db=db)
    return result