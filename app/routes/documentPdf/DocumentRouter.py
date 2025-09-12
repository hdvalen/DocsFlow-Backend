from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlmodel import Session
from app.database.database import get_db
from app.controllers.documents.documentsController import guardar_documento, get_documents_by_user, get_documents_by_id, get_all_documents, delete_document
from app.models.Document.DocumentModel import DocumentCreate
from app.auth.dependencies import get_current_user, JWTBearer
from app.auth.dependencies import role_required

router = APIRouter(tags=["Documents"])


@router.post("/", dependencies=[Depends(JWTBearer())])
async def upload_document(
    file: UploadFile = File(...),
    department_id: int = Form(...),
    uploaded_by: int = Form(...),
    doc_type_id: int = Form(...),
    company_id: int = Form(...),
    title: str = Form(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # 🔒 Validación de permisos
    if current_user["role"] != "admin":
        # Usuarios normales solo pueden subir documentos a su empresa y departamento
        if company_id != current_user["company_id"] or department_id != current_user["department_id"]:
            raise HTTPException(
                status_code=403,
                detail="No tienes permisos para subir documentos a esta empresa o departamento"
            )
        uploaded_by = current_user["id"]  # asegurarse que solo se registre su propio ID

    doc_data = DocumentCreate(
        department_id=department_id,
        uploaded_by=uploaded_by,
        doc_type_id=doc_type_id,
        company_id=company_id,
        title=title
    )

    doc = guardar_documento(file=file, doc_data=doc_data, db=db)

    return {"message": "Documento guardado correctamente", "document": doc}


@router.get("/user/{user_id}", dependencies=[Depends(JWTBearer())])
def read_documents_by_user(user_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # 🔒 Validación de permisos
    if current_user["role"] != "admin":
        if user_id != current_user["id"]:
            raise HTTPException(status_code=403, detail="No puedes ver documentos de otros usuarios")

    documents = get_documents_by_user(user_id=user_id, db=db)
    return {"documents": documents}


@router.get("/{document_id}", dependencies=[Depends(JWTBearer())])
def read_document_by_id(document_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
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

    if not document:
        raise HTTPException(status_code=404, detail="Documento no encontrado")

    # 🔒 Validación de permisos
    if current_user["role"] != "admin":
        if document.company_id != current_user["company_id"] or document.department_id != current_user["department_id"]:
            raise HTTPException(
                status_code=403,
                detail="No tienes permisos para ver este documento"
            )

    return {"document": document}

