from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from session.security import get_user_id_from_access_token
from users.user_roles.dependencies import require_coach_role, require_admin_role, require_coach_or_admin
from . import crud, schemas

router = APIRouter(prefix="/coaches", tags=["coaches"])


@router.post("/", response_model=schemas.Coach)
def create_coach(
    coach: schemas.CoachCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_user_id_from_access_token),
    _: bool = Depends(require_coach_or_admin)
):
    """Crear un nuevo perfil de entrenador"""
    return crud.create_coach(db=db, coach=coach, user_id=current_user_id)


@router.get("/", response_model=List[schemas.Coach])
def read_coaches(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtener lista de entrenadores"""
    coaches = crud.get_coaches(db, skip=skip, limit=limit)
    return coaches


@router.get("/me", response_model=schemas.Coach)
def get_my_coach_profile(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_user_id_from_access_token),
    _: bool = Depends(require_coach_role)
):
    """Obtener mi perfil de entrenador"""
    coach = crud.get_coach_by_user_id(db, user_id=current_user_id)
    if coach is None:
        raise HTTPException(status_code=404, detail="Perfil de entrenador no encontrado")
    return coach


@router.get("/{coach_id}", response_model=schemas.Coach)
def read_coach(
    coach_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtener entrenador por ID"""
    coach = crud.get_coach(db, coach_id=coach_id)
    if coach is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entrenador no encontrado"
        )
    return coach


@router.put("/{coach_id}", response_model=schemas.Coach)
def update_coach(
    coach_id: int,
    coach_update: schemas.CoachUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualizar entrenador"""
    # Verificar que el usuario actual sea el entrenador o tenga permisos
    coach = crud.get_coach(db, coach_id=coach_id)
    if not coach:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entrenador no encontrado"
        )
    
    if coach.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para actualizar este entrenador"
        )
    
    updated_coach = crud.update_coach(db=db, coach_id=coach_id, coach_update=coach_update)
    return updated_coach


@router.delete("/{coach_id}")
def delete_coach(
    coach_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Eliminar entrenador"""
    coach = crud.get_coach(db, coach_id=coach_id)
    if not coach:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entrenador no encontrado"
        )
    
    if coach.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para eliminar este entrenador"
        )
    
    success = crud.delete_coach(db=db, coach_id=coach_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo eliminar el entrenador"
        )
    
    return {"message": "Entrenador eliminado exitosamente"}


# Endpoints para relaciones entrenador-alumno
@router.post("/students", response_model=schemas.CoachStudent)
def add_student(
    relationship: schemas.CoachStudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Agregar alumno a entrenador"""
    # Verificar que el usuario actual sea el entrenador
    coach = crud.get_coach(db, coach_id=relationship.coach_id)
    if not coach or coach.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para agregar alumnos a este entrenador"
        )
    
    # Verificar que no exista ya la relación
    existing = crud.get_coach_student_relationship(db, relationship.coach_id, relationship.student_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La relación entrenador-alumno ya existe"
        )
    
    return crud.create_coach_student_relationship(db=db, relationship=relationship)


@router.get("/me/students", response_model=List[schemas.CoachStudent])
def get_my_students(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtener alumnos del entrenador actual"""
    coach = crud.get_coach_by_user_id(db, current_user.id)
    if not coach:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entrenador no encontrado"
        )
    
    return crud.get_coach_students(db, coach.id)


@router.put("/students/{relationship_id}", response_model=schemas.CoachStudent)
def update_student_relationship(
    relationship_id: int,
    relationship_update: schemas.CoachStudentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualizar relación entrenador-alumno"""
    relationship = db.query(crud.models.CoachStudent).filter(
        crud.models.CoachStudent.id == relationship_id
    ).first()
    
    if not relationship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relación no encontrada"
        )
    
    # Verificar permisos
    coach = crud.get_coach(db, relationship.coach_id)
    if not coach or coach.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para actualizar esta relación"
        )
    
    return crud.update_coach_student_relationship(db=db, relationship_id=relationship_id, relationship_update=relationship_update)


@router.delete("/students/{student_id}")
def remove_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remover alumno del entrenador"""
    coach = crud.get_coach_by_user_id(db, current_user.id)
    if not coach:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entrenador no encontrado"
        )
    
    success = crud.end_coach_student_relationship(db=db, coach_id=coach.id, student_id=student_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo remover el alumno"
        )
    
    return {"message": "Alumno removido exitosamente"}