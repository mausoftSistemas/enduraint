from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class GoalStatusEnum(str, Enum):
    """Estados de los objetivos"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class GoalTypeEnum(str, Enum):
    """Tipos de objetivos"""
    DISTANCE = "distance"
    TIME = "time"
    WEIGHT_LOSS = "weight_loss"
    STRENGTH = "strength"
    ENDURANCE = "endurance"
    TECHNIQUE = "technique"
    CUSTOM = "custom"


class TrainingGoalBase(BaseModel):
    """Esquema base para objetivos de entrenamiento"""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    goal_type: GoalTypeEnum
    target_value: Optional[float] = None
    current_value: float = 0
    unit: Optional[str] = None
    target_date: Optional[datetime] = None
    status: GoalStatusEnum = GoalStatusEnum.PENDING
    priority: str = "medium"
    is_active: bool = True


class TrainingGoalCreate(TrainingGoalBase):
    """Esquema para crear objetivo de entrenamiento"""
    coach_id: int
    student_id: int


class TrainingGoalUpdate(TrainingGoalBase):
    """Esquema para actualizar objetivo de entrenamiento"""
    title: Optional[str] = None
    goal_type: Optional[GoalTypeEnum] = None


class TrainingGoal(TrainingGoalBase):
    """Esquema completo del objetivo de entrenamiento"""
    id: int
    coach_id: int
    student_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TrainingFeedbackBase(BaseModel):
    """Esquema base para feedback de entrenamiento"""
    feedback_type: str = "general"
    title: Optional[str] = None
    content: str = Field(..., min_length=1)
    rating: Optional[int] = Field(None, ge=1, le=5)
    is_private: bool = False


class TrainingFeedbackCreate(TrainingFeedbackBase):
    """Esquema para crear feedback de entrenamiento"""
    coach_id: int
    student_id: int
    goal_id: Optional[int] = None
    activity_id: Optional[int] = None


class TrainingFeedbackUpdate(TrainingFeedbackBase):
    """Esquema para actualizar feedback de entrenamiento"""
    content: Optional[str] = None


class TrainingFeedback(TrainingFeedbackBase):
    """Esquema completo del feedback de entrenamiento"""
    id: int
    coach_id: int
    student_id: int
    goal_id: Optional[int] = None
    activity_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TrainingGoalWithFeedback(TrainingGoal):
    """Esquema de objetivo con feedback asociado"""
    feedback: List[TrainingFeedback] = []

    class Config:
        from_attributes = True


class TrainingGoalProgress(BaseModel):
    """Esquema para actualizar progreso de objetivo"""
    current_value: float
    status: Optional[GoalStatusEnum] = None
    notes: Optional[str] = None