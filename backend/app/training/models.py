from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database_sqlite import Base
import enum


class GoalStatus(enum.Enum):
    """Estados de los objetivos de entrenamiento"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class GoalType(enum.Enum):
    """Tipos de objetivos de entrenamiento"""
    DISTANCE = "distance"
    TIME = "time"
    WEIGHT_LOSS = "weight_loss"
    STRENGTH = "strength"
    ENDURANCE = "endurance"
    TECHNIQUE = "technique"
    CUSTOM = "custom"


class TrainingGoal(Base):
    """Modelo para objetivos de entrenamiento personalizados"""
    __tablename__ = "training_goals"

    id = Column(Integer, primary_key=True, index=True)
    coach_id = Column(Integer, index=True)  # FK a coaches
    student_id = Column(Integer, index=True)  # FK a students
    title = Column(String(255), nullable=False)
    description = Column(Text)
    goal_type = Column(Enum(GoalType), nullable=False)
    target_value = Column(Float)  # Valor objetivo (distancia, tiempo, peso, etc.)
    current_value = Column(Float, default=0)  # Valor actual
    unit = Column(String(50))  # Unidad de medida (km, min, kg, etc.)
    target_date = Column(DateTime)
    status = Column(Enum(GoalStatus), default=GoalStatus.PENDING)
    priority = Column(String(20), default="medium")  # high, medium, low
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relaciones
    coach = relationship("Coach", back_populates="training_goals")
    student = relationship("Student", back_populates="training_goals")
    feedback = relationship("TrainingFeedback", back_populates="goal")


class TrainingFeedback(Base):
    """Modelo para feedback y comentarios entre entrenador-alumno"""
    __tablename__ = "training_feedback"

    id = Column(Integer, primary_key=True, index=True)
    coach_id = Column(Integer, index=True)  # FK a coaches
    student_id = Column(Integer, index=True)  # FK a students
    goal_id = Column(Integer, index=True, nullable=True)  # FK a training_goals (opcional)
    activity_id = Column(Integer, index=True, nullable=True)  # FK a activities (opcional)
    feedback_type = Column(String(50))  # general, goal_specific, activity_specific
    title = Column(String(255))
    content = Column(Text, nullable=False)
    rating = Column(Integer)  # Calificación del 1 al 5
    is_private = Column(Boolean, default=False)  # Si es privado solo para el alumno
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relaciones
    coach = relationship("Coach", back_populates="feedback_given")
    student = relationship("Student", back_populates="feedback_received")
    goal = relationship("TrainingGoal", back_populates="feedback")