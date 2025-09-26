from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database_sqlite import Base


class Coach(Base):
    """Modelo para entrenadores"""
    __tablename__ = "coaches"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, unique=True)  # Referencia al usuario base
    specialization = Column(String(255))  # Especialización del entrenador
    certification = Column(String(255))  # Certificaciones
    experience_years = Column(Integer)  # Años de experiencia
    bio = Column(Text)  # Biografía del entrenador
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relaciones
    students = relationship("CoachStudent", back_populates="coach")
    training_goals = relationship("TrainingGoal", back_populates="coach")
    feedback_given = relationship("TrainingFeedback", back_populates="coach")


class CoachStudent(Base):
    """Modelo para la relación entrenador-alumno"""
    __tablename__ = "coach_students"

    id = Column(Integer, primary_key=True, index=True)
    coach_id = Column(Integer, index=True)  # FK a coaches
    student_id = Column(Integer, index=True)  # FK a students
    start_date = Column(DateTime, server_default=func.now())
    end_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    notes = Column(Text)  # Notas del entrenador sobre el alumno
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relaciones
    coach = relationship("Coach", back_populates="students")
    student = relationship("Student", back_populates="coaches")