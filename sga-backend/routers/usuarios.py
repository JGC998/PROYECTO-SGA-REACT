from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
import models
from schemas import UsuarioResponse, UsuarioCreate, UsuarioBase
from auth.dependencies import require_admin
from auth.jwt import get_password_hash

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(skip: int = 0, limit: int = 50, db: Session = Depends(get_db),
                    current_user: models.Usuario = Depends(require_admin)):
    return db.query(models.Usuario).order_by(models.Usuario.id).offset(skip).limit(limit).all()


@router.post("/", response_model=UsuarioResponse)
def crear_usuario(item: UsuarioCreate, db: Session = Depends(get_db),
                  current_user: models.Usuario = Depends(require_admin)):
    if db.query(models.Usuario).filter(models.Usuario.email == item.email).first():
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    nuevo_usuario = models.Usuario(
        nombre=item.nombre,
        email=item.email,
        rol=item.rol,
        password_hash=get_password_hash(item.password),
        activo=item.activo,
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def actualizar_usuario(usuario_id: int, item: UsuarioBase, db: Session = Depends(get_db),
                       current_user: models.Usuario = Depends(require_admin)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
    usuario.nombre = item.nombre
    usuario.rol = item.rol
    usuario.activo = item.activo
    # El email normalmente no se cambia, pero si se cambia habría que verificar si ya existe
    
    db.commit()
    db.refresh(usuario)
    return usuario


@router.delete("/{usuario_id}")
def desactivar_usuario(usuario_id: int, db: Session = Depends(get_db),
                       current_user: models.Usuario = Depends(require_admin)):
    # Los usuarios se desactivan, nunca se borran para no romper logs / historial
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
    if usuario.id == current_user.id:
        raise HTTPException(status_code=400, detail="No puedes desactivar tu propio usuario")
        
    usuario.activo = False
    db.commit()
    return {"message": "Usuario desactivado correctamente"}
