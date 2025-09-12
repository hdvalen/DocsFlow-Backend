from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlmodel import Session
from app.database.database import get_db
from app.controllers.documents.documentsController import guardar_documento, get_documents_by_user, get_documents_by_id, get_all_documents, delete_document
from app.models.Document.DocumentModel import DocumentCreate, Document
from app.auth.dependencies import get_current_user, JWTBearer, role_required

router = APIRouter(tags=["Documents"])


@router.post("/", dependencies=[Depends(JWTBearer())])
async def upload_document(
    file: UploadFile = File(...),
    department_id: int = Form(...),
    doc_type_id: int = Form(...),
    company_id: int = Form(...),
    title: str = Form(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
   
    uploaded_by = current_user["id"]  # asegurarse que solo se registre su propio ID

    doc_data = DocumentCreate(
        department_id=department_id,
        uploaded_by=uploaded_by,
        doc_type_id=doc_type_id,
        company_id=company_id,
        title=title
    )

    doc = guardar_documento(
    file=file,
    doc_data=doc_data,
    uploaded_by=uploaded_by,
    db=db
    )

    return {"message": "Documento guardado correctamente", "document": doc}


@router.get("/user/{user_id}", dependencies=[Depends(get_current_user)])
def read_documents_by_user(user_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    #  Validación de permisos
    if current_user["role"] != "admin":
        if user_id != current_user["id"]:
            raise HTTPException(status_code=403, detail="No puedes ver documentos de otros usuarios")

    documents = get_documents_by_user(user_id=user_id, db=db)
    return {"documents": documents}


@router.get("/{document_id}", dependencies=[Depends(get_current_user)])
def read_document_by_id(document_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    document = get_documents_by_id(document_id=document_id, db=db)
    # verificacion de roles para los permisos de acceso
    if current_user["role"] != "admin":
        if document.company_id != current_user["company_id"] or document.department_id != current_user["department_id"]:
            raise HTTPException(status_code=403, detail="No tienes permisos para ver este documento")

    return {"documento": document}

 # solo admin puede ver todos los documentos
@router.get("/", dependencies=[Depends(role_required(["admin"]))])
def read_all_documents(db: Session = Depends(get_db)):
    documents = get_all_documents(db=db)
    return {"documents": documents}

# administrador puede eliminar cualquier documento
# usuarios solo pueden eliminar sus documentos 
@router.delete("/{document_id}", dependencies=[Depends(JWTBearer())])
def delete_document_route(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Buscar el documento
    document = db.query(Document).filter(Document.id == document_id).first()

    if not document:
        raise HTTPException(status_code=404, detail="Documento no encontrado")

    # 🔒 Validación de permisos
    if current_user["role"] != "admin":
        # Solo puede eliminar sus propios documentos
        if document.uploaded_by != current_user["id"]:
            raise HTTPException(
                status_code=403,
                detail="No tienes permisos para eliminar este documento"
            )

    # Eliminar el documento
    db.delete(document)
    db.commit()

    return {"detail": "Documento eliminado correctamente"}