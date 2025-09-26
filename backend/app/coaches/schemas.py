from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CoachBase(BaseModel):
    """Esquema base para entrenadores"""
    specialization: Optional[str] = None
    certification: Optional[str] = None
    experience_years: Optional[int] = None
    bio: Optional[str] = None
    is_active: bool = True


class CoachCreate(CoachBase):
    """Esquema para crear un entrenador"""
    user_id: int


class CoachUpdate(CoachBase):
    """Esquema para actualizar un entrenador"""
    pass


class Coach(CoachBase):
    """Esquema completo del entrenador"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CoachStudentBase(BaseModel):
    """Esquema base para relación entrenador-alumno"""
    notes: Optional[str] = None
    is_active: bool = True


class CoachStudentCreate(CoachStudentBase):
    """Esquema para crear relación entrenador-alumno"""
    coach_id: int
    student_id: int


class CoachStudentUpdate(CoachStudentBase):
    """Esquema para actualizar relación entrenador-alumno"""
    end_date: Optional[datetime] = None


class CoachStudent(CoachStudentBase):
    """Esquema completo de relación entrenador-alumno"""
    id: int
    coach_id: int
    student_id: int
    start_date: datetime
    end_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CoachWithStudents(Coach):
    """Esquema de entrenador con sus alumnos"""
    students: List[CoachStudent] = []

    class Config:
        from_attributes = True