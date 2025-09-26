from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas


def get_student(db: Session, student_id: int) -> Optional[models.Student]:
    """Obtener estudiante por ID"""
    return db.query(models.Student).filter(models.Student.id == student_id).first()


def get_student_by_user_id(db: Session, user_id: int) -> Optional[models.Student]:
    """Obtener estudiante por ID de usuario"""
    return db.query(models.Student).filter(models.Student.user_id == user_id).first()


def get_students(db: Session, skip: int = 0, limit: int = 100) -> List[models.Student]:
    """Obtener lista de estudiantes"""
    return db.query(models.Student).filter(models.Student.is_active == True).offset(skip).limit(limit).all()


def create_student(db: Session, student: schemas.StudentCreate) -> models.Student:
    """Crear nuevo estudiante"""
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def update_student(db: Session, student_id: int, student_update: schemas.StudentUpdate) -> Optional[models.Student]:
    """Actualizar estudiante"""
    db_student = get_student(db, student_id)
    if db_student:
        update_data = student_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_student, field, value)
        db.commit()
        db.refresh(db_student)
    return db_student


def delete_student(db: Session, student_id: int) -> bool:
    """Eliminar estudiante (soft delete)"""
    db_student = get_student(db, student_id)
    if db_student:
        db_student.is_active = False
        db.commit()
        return True
    return False


# CRUD para registros de progreso
def get_progress_record(db: Session, record_id: int) -> Optional[models.ProgressRecord]:
    """Obtener registro de progreso por ID"""
    return db.query(models.ProgressRecord).filter(models.ProgressRecord.id == record_id).first()


def get_student_progress_records(db: Session, student_id: int, skip: int = 0, limit: int = 100) -> List[models.ProgressRecord]:
    """Obtener registros de progreso de un estudiante"""
    return db.query(models.ProgressRecord).filter(
        models.ProgressRecord.student_id == student_id
    ).order_by(models.ProgressRecord.record_date.desc()).offset(skip).limit(limit).all()


def get_latest_progress_record(db: Session, student_id: int) -> Optional[models.ProgressRecord]:
    """Obtener el último registro de progreso de un estudiante"""
    return db.query(models.ProgressRecord).filter(
        models.ProgressRecord.student_id == student_id
    ).order_by(models.ProgressRecord.record_date.desc()).first()


def create_progress_record(db: Session, progress: schemas.ProgressRecordCreate) -> models.ProgressRecord:
    """Crear nuevo registro de progreso"""
    db_progress = models.ProgressRecord(**progress.dict())
    if not db_progress.record_date:
        from datetime import datetime
        db_progress.record_date = datetime.now()
    db.add(db_progress)
    db.commit()
    db.refresh(db_progress)
    return db_progress


def update_progress_record(db: Session, record_id: int, progress_update: schemas.ProgressRecordUpdate) -> Optional[models.ProgressRecord]:
    """Actualizar registro de progreso"""
    db_progress = get_progress_record(db, record_id)
    if db_progress:
        update_data = progress_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_progress, field, value)
        db.commit()
        db.refresh(db_progress)
    return db_progress


def delete_progress_record(db: Session, record_id: int) -> bool:
    """Eliminar registro de progreso"""
    db_progress = get_progress_record(db, record_id)
    if db_progress:
        db.delete(db_progress)
        db.commit()
        return True
    return False


def get_progress_summary(db: Session, student_id: int) -> dict:
    """Obtener resumen de progreso del estudiante"""
    records = get_student_progress_records(db, student_id, limit=1000)
    if not records:
        return {}
    
    latest = records[0]
    oldest = records[-1] if len(records) > 1 else latest
    
    summary = {
        "total_records": len(records),
        "latest_record": {
            "date": latest.record_date,
            "weight": latest.weight,
            "body_fat_percentage": latest.body_fat_percentage,
            "muscle_mass": latest.muscle_mass
        },
        "progress": {}
    }
    
    if len(records) > 1:
        if latest.weight and oldest.weight:
            summary["progress"]["weight_change"] = latest.weight - oldest.weight
        if latest.body_fat_percentage and oldest.body_fat_percentage:
            summary["progress"]["body_fat_change"] = latest.body_fat_percentage - oldest.body_fat_percentage
        if latest.muscle_mass and oldest.muscle_mass:
            summary["progress"]["muscle_mass_change"] = latest.muscle_mass - oldest.muscle_mass
    
    return summary