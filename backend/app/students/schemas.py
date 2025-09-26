from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class StudentBase(BaseModel):
    """Esquema base para estudiantes"""
    fitness_level: Optional[str] = None
    goals: Optional[str] = None
    medical_notes: Optional[str] = None
    preferred_activities: Optional[str] = None
    current_weight: Optional[float] = None
    target_weight: Optional[float] = None
    is_active: bool = True


class StudentCreate(StudentBase):
    """Esquema para crear un estudiante"""
    user_id: int


class StudentUpdate(StudentBase):
    """Esquema para actualizar un estudiante"""
    pass


class Student(StudentBase):
    """Esquema completo del estudiante"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProgressRecordBase(BaseModel):
    """Esquema base para registros de progreso"""
    weight: Optional[float] = None
    body_fat_percentage: Optional[float] = None
    muscle_mass: Optional[float] = None
    notes: Optional[str] = None


class ProgressRecordCreate(ProgressRecordBase):
    """Esquema para crear registro de progreso"""
    student_id: int
    record_date: Optional[datetime] = None


class ProgressRecordUpdate(ProgressRecordBase):
    """Esquema para actualizar registro de progreso"""
    pass


class ProgressRecord(ProgressRecordBase):
    """Esquema completo del registro de progreso"""
    id: int
    student_id: int
    record_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class StudentWithProgress(Student):
    """Esquema de estudiante con registros de progreso"""
    progress_records: List[ProgressRecord] = []

    class Config:
        from_attributes = True


class StudentWithCoaches(Student):
    """Esquema de estudiante con sus entrenadores"""
    coaches: List['CoachStudent'] = []

    class Config:
        from_attributes = True


# Importar después para evitar referencias circulares
from coaches.schemas import CoachStudent
StudentWithCoaches.model_rebuild()