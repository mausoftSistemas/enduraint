from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database_sqlite import Base


class Student(Base):
    """Modelo para estudiantes/alumnos"""
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, unique=True)  # Referencia al usuario base
    fitness_level = Column(String(50))  # Nivel de condición física (beginner, intermediate, advanced)
    goals = Column(Text)  # Objetivos personales del alumno
    medical_notes = Column(Text)  # Notas médicas o restricciones
    preferred_activities = Column(String(500))  # Actividades preferidas
    current_weight = Column(Float)  # Peso actual
    target_weight = Column(Float)  # Peso objetivo
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relaciones
    coaches = relationship("CoachStudent", back_populates="student")
    training_goals = relationship("TrainingGoal", back_populates="student")
    feedback_received = relationship("TrainingFeedback", back_populates="student")
    progress_records = relationship("ProgressRecord", back_populates="student")


class ProgressRecord(Base):
    """Modelo para registros de progreso del estudiante"""
    __tablename__ = "progress_records"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, index=True)  # FK a students
    record_date = Column(DateTime, server_default=func.now())
    weight = Column(Float)
    body_fat_percentage = Column(Float)
    muscle_mass = Column(Float)
    notes = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    # Relaciones
    student = relationship("Student", back_populates="progress_records")