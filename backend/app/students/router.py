from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from session.security import get_user_id_from_access_token
from users.user_roles.dependencies import require_student_role, require_coach_role, require_coach_or_admin, verify_coach_student_access
from . import crud, schemas

router = APIRouter(prefix="/students", tags=["students"])


@router.post("/", response_model=schemas.Student)
def create_student(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_user_id_from_access_token),
    _: bool = Depends(require_student_role)
):
    """Crear un nuevo perfil de alumno"""
    return crud.create_student(db=db, student=student, user_id=current_user_id)


@router.get("/", response_model=List[schemas.Student])
def read_students(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtener lista de estudiantes"""
    students = crud.get_students(db, skip=skip, limit=limit)
    return students


@router.get("/me", response_model=schemas.Student)
def get_my_student_profile(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_user_id_from_access_token),
    _: bool = Depends(require_student_role)
):
    """Obtener mi perfil de alumno"""
    student = crud.get_student_by_user_id(db, user_id=current_user_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Perfil de alumno no encontrado")
    return student


@router.get("/{student_id}", response_model=schemas.Student)
def read_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtener estudiante por ID"""
    student = crud.get_student(db, student_id=student_id)
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado"
        )
    return student


@router.put("/{student_id}", response_model=schemas.Student)
def update_student(
    student_id: int,
    student_update: schemas.StudentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualizar estudiante"""
    # Verificar que el usuario actual sea el estudiante o su entrenador
    student = crud.get_student(db, student_id=student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado"
        )
    
    # Verificar permisos: el propio estudiante o su entrenador
    if student.user_id != current_user.id:
        # Verificar si el usuario actual es entrenador del estudiante
        from coaches.crud import get_coach_by_user_id, get_coach_student_relationship
        coach = get_coach_by_user_id(db, current_user.id)
        if not coach or not get_coach_student_relationship(db, coach.id, student_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para actualizar este estudiante"
            )
    
    updated_student = crud.update_student(db=db, student_id=student_id, student_update=student_update)
    return updated_student


@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Eliminar estudiante"""
    student = crud.get_student(db, student_id=student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado"
        )
    
    if student.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para eliminar este estudiante"
        )
    
    success = crud.delete_student(db=db, student_id=student_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo eliminar el estudiante"
        )
    
    return {"message": "Estudiante eliminado exitosamente"}


# Endpoints para registros de progreso
@router.post("/progress", response_model=schemas.ProgressRecord)
def create_progress_record(
    progress: schemas.ProgressRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crear registro de progreso"""
    # Verificar permisos: el estudiante o su entrenador
    student = crud.get_student(db, progress.student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado"
        )
    
    if student.user_id != current_user.id:
        # Verificar si es el entrenador
        from coaches.crud import get_coach_by_user_id, get_coach_student_relationship
        coach = get_coach_by_user_id(db, current_user.id)
        if not coach or not get_coach_student_relationship(db, coach.id, progress.student_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para crear registros de progreso para este estudiante"
            )
    
    return crud.create_progress_record(db=db, progress=progress)


@router.get("/me/progress", response_model=List[schemas.ProgressRecord])
def get_my_progress(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtener registros de progreso del estudiante actual"""
    student = crud.get_student_by_user_id(db, current_user.id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado"
        )
    
    return crud.get_student_progress_records(db, student.id, skip=skip, limit=limit)


@router.get("/{student_id}/progress", response_model=List[schemas.ProgressRecord])
def get_student_progress(
    student_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtener registros de progreso de un estudiante"""
    # Verificar permisos: el estudiante o su entrenador
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado"
        )
    
    if student.user_id != current_user.id:
        # Verificar si es el entrenador
        from coaches.crud import get_coach_by_user_id, get_coach_student_relationship
        coach = get_coach_by_user_id(db, current_user.id)
        if not coach or not get_coach_student_relationship(db, coach.id, student_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para ver el progreso de este estudiante"
            )
    
    return crud.get_student_progress_records(db, student_id, skip=skip, limit=limit)


@router.get("/me/progress/summary")
def get_my_progress_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtener resumen de progreso del estudiante actual"""
    student = crud.get_student_by_user_id(db, current_user.id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado"
        )
    
    return crud.get_progress_summary(db, student.id)


@router.get("/{student_id}/progress/summary")
def get_student_progress_summary(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtener resumen de progreso de un estudiante"""
    # Verificar permisos: el estudiante o su entrenador
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado"
        )
    
    if student.user_id != current_user.id:
        # Verificar si es el entrenador
        from coaches.crud import get_coach_by_user_id, get_coach_student_relationship
        coach = get_coach_by_user_id(db, current_user.id)
        if not coach or not get_coach_student_relationship(db, coach.id, student_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para ver el progreso de este estudiante"
            )
    
    return crud.get_progress_summary(db, student_id)


@router.put("/progress/{record_id}", response_model=schemas.ProgressRecord)
def update_progress_record(
    record_id: int,
    progress_update: schemas.ProgressRecordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualizar registro de progreso"""
    record = crud.get_progress_record(db, record_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de progreso no encontrado"
        )
    
    # Verificar permisos
    student = crud.get_student(db, record.student_id)
    if student.user_id != current_user.id:
        # Verificar si es el entrenador
        from coaches.crud import get_coach_by_user_id, get_coach_student_relationship
        coach = get_coach_by_user_id(db, current_user.id)
        if not coach or not get_coach_student_relationship(db, coach.id, record.student_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para actualizar este registro"
            )
    
    return crud.update_progress_record(db=db, record_id=record_id, progress_update=progress_update)


@router.delete("/progress/{record_id}")
def delete_progress_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Eliminar registro de progreso"""
    record = crud.get_progress_record(db, record_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de progreso no encontrado"
        )
    
    # Verificar permisos
    student = crud.get_student(db, record.student_id)
    if student.user_id != current_user.id:
        # Verificar si es el entrenador
        from coaches.crud import get_coach_by_user_id, get_coach_student_relationship
        coach = get_coach_by_user_id(db, current_user.id)
        if not coach or not get_coach_student_relationship(db, coach.id, record.student_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para eliminar este registro"
            )
    
    success = crud.delete_progress_record(db=db, record_id=record_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo eliminar el registro de progreso"
        )
    
    return {"message": "Registro de progreso eliminado exitosamente"}