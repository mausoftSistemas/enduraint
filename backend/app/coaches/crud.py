from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas


def get_coach(db: Session, coach_id: int) -> Optional[models.Coach]:
    """Obtener entrenador por ID"""
    return db.query(models.Coach).filter(models.Coach.id == coach_id).first()


def get_coach_by_user_id(db: Session, user_id: int) -> Optional[models.Coach]:
    """Obtener entrenador por ID de usuario"""
    return db.query(models.Coach).filter(models.Coach.user_id == user_id).first()


def get_coaches(db: Session, skip: int = 0, limit: int = 100) -> List[models.Coach]:
    """Obtener lista de entrenadores"""
    return db.query(models.Coach).filter(models.Coach.is_active == True).offset(skip).limit(limit).all()


def create_coach(db: Session, coach: schemas.CoachCreate) -> models.Coach:
    """Crear nuevo entrenador"""
    db_coach = models.Coach(**coach.dict())
    db.add(db_coach)
    db.commit()
    db.refresh(db_coach)
    return db_coach


def update_coach(db: Session, coach_id: int, coach_update: schemas.CoachUpdate) -> Optional[models.Coach]:
    """Actualizar entrenador"""
    db_coach = get_coach(db, coach_id)
    if db_coach:
        update_data = coach_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_coach, field, value)
        db.commit()
        db.refresh(db_coach)
    return db_coach


def delete_coach(db: Session, coach_id: int) -> bool:
    """Eliminar entrenador (soft delete)"""
    db_coach = get_coach(db, coach_id)
    if db_coach:
        db_coach.is_active = False
        db.commit()
        return True
    return False


# CRUD para relaciones entrenador-alumno
def get_coach_student_relationship(db: Session, coach_id: int, student_id: int) -> Optional[models.CoachStudent]:
    """Obtener relación entrenador-alumno"""
    return db.query(models.CoachStudent).filter(
        models.CoachStudent.coach_id == coach_id,
        models.CoachStudent.student_id == student_id,
        models.CoachStudent.is_active == True
    ).first()


def get_coach_students(db: Session, coach_id: int) -> List[models.CoachStudent]:
    """Obtener todos los alumnos de un entrenador"""
    return db.query(models.CoachStudent).filter(
        models.CoachStudent.coach_id == coach_id,
        models.CoachStudent.is_active == True
    ).all()


def get_student_coaches(db: Session, student_id: int) -> List[models.CoachStudent]:
    """Obtener todos los entrenadores de un alumno"""
    return db.query(models.CoachStudent).filter(
        models.CoachStudent.student_id == student_id,
        models.CoachStudent.is_active == True
    ).all()


def create_coach_student_relationship(db: Session, relationship: schemas.CoachStudentCreate) -> models.CoachStudent:
    """Crear relación entrenador-alumno"""
    db_relationship = models.CoachStudent(**relationship.dict())
    db.add(db_relationship)
    db.commit()
    db.refresh(db_relationship)
    return db_relationship


def update_coach_student_relationship(db: Session, relationship_id: int, relationship_update: schemas.CoachStudentUpdate) -> Optional[models.CoachStudent]:
    """Actualizar relación entrenador-alumno"""
    db_relationship = db.query(models.CoachStudent).filter(models.CoachStudent.id == relationship_id).first()
    if db_relationship:
        update_data = relationship_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_relationship, field, value)
        db.commit()
        db.refresh(db_relationship)
    return db_relationship


def end_coach_student_relationship(db: Session, coach_id: int, student_id: int) -> bool:
    """Finalizar relación entrenador-alumno"""
    db_relationship = get_coach_student_relationship(db, coach_id, student_id)
    if db_relationship:
        db_relationship.is_active = False
        from datetime import datetime
        db_relationship.end_date = datetime.now()
        db.commit()
        return True
    return False