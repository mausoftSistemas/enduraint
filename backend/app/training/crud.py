from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas
from datetime import datetime


# CRUD para objetivos de entrenamiento
def get_training_goal(db: Session, goal_id: int) -> Optional[models.TrainingGoal]:
    """Obtener objetivo de entrenamiento por ID"""
    return db.query(models.TrainingGoal).filter(models.TrainingGoal.id == goal_id).first()


def get_coach_goals(db: Session, coach_id: int, skip: int = 0, limit: int = 100) -> List[models.TrainingGoal]:
    """Obtener objetivos creados por un entrenador"""
    return db.query(models.TrainingGoal).filter(
        models.TrainingGoal.coach_id == coach_id,
        models.TrainingGoal.is_active == True
    ).offset(skip).limit(limit).all()


def get_student_goals(db: Session, student_id: int, skip: int = 0, limit: int = 100) -> List[models.TrainingGoal]:
    """Obtener objetivos asignados a un estudiante"""
    return db.query(models.TrainingGoal).filter(
        models.TrainingGoal.student_id == student_id,
        models.TrainingGoal.is_active == True
    ).offset(skip).limit(limit).all()


def get_goals_by_status(db: Session, student_id: int, status: models.GoalStatus) -> List[models.TrainingGoal]:
    """Obtener objetivos por estado"""
    return db.query(models.TrainingGoal).filter(
        models.TrainingGoal.student_id == student_id,
        models.TrainingGoal.status == status,
        models.TrainingGoal.is_active == True
    ).all()


def create_training_goal(db: Session, goal: schemas.TrainingGoalCreate) -> models.TrainingGoal:
    """Crear nuevo objetivo de entrenamiento"""
    db_goal = models.TrainingGoal(**goal.dict())
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal


def update_training_goal(db: Session, goal_id: int, goal_update: schemas.TrainingGoalUpdate) -> Optional[models.TrainingGoal]:
    """Actualizar objetivo de entrenamiento"""
    db_goal = get_training_goal(db, goal_id)
    if db_goal:
        update_data = goal_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_goal, field, value)
        db.commit()
        db.refresh(db_goal)
    return db_goal


def update_goal_progress(db: Session, goal_id: int, progress: schemas.TrainingGoalProgress) -> Optional[models.TrainingGoal]:
    """Actualizar progreso de objetivo"""
    db_goal = get_training_goal(db, goal_id)
    if db_goal:
        db_goal.current_value = progress.current_value
        if progress.status:
            db_goal.status = progress.status
        
        # Auto-completar si se alcanza el objetivo
        if db_goal.target_value and db_goal.current_value >= db_goal.target_value:
            db_goal.status = models.GoalStatus.COMPLETED
        
        db.commit()
        db.refresh(db_goal)
    return db_goal


def delete_training_goal(db: Session, goal_id: int) -> bool:
    """Eliminar objetivo de entrenamiento (soft delete)"""
    db_goal = get_training_goal(db, goal_id)
    if db_goal:
        db_goal.is_active = False
        db.commit()
        return True
    return False


# CRUD para feedback de entrenamiento
def get_training_feedback(db: Session, feedback_id: int) -> Optional[models.TrainingFeedback]:
    """Obtener feedback por ID"""
    return db.query(models.TrainingFeedback).filter(models.TrainingFeedback.id == feedback_id).first()


def get_coach_feedback(db: Session, coach_id: int, skip: int = 0, limit: int = 100) -> List[models.TrainingFeedback]:
    """Obtener feedback dado por un entrenador"""
    return db.query(models.TrainingFeedback).filter(
        models.TrainingFeedback.coach_id == coach_id
    ).order_by(models.TrainingFeedback.created_at.desc()).offset(skip).limit(limit).all()


def get_student_feedback(db: Session, student_id: int, skip: int = 0, limit: int = 100) -> List[models.TrainingFeedback]:
    """Obtener feedback recibido por un estudiante"""
    return db.query(models.TrainingFeedback).filter(
        models.TrainingFeedback.student_id == student_id
    ).order_by(models.TrainingFeedback.created_at.desc()).offset(skip).limit(limit).all()


def get_goal_feedback(db: Session, goal_id: int) -> List[models.TrainingFeedback]:
    """Obtener feedback específico de un objetivo"""
    return db.query(models.TrainingFeedback).filter(
        models.TrainingFeedback.goal_id == goal_id
    ).order_by(models.TrainingFeedback.created_at.desc()).all()


def get_activity_feedback(db: Session, activity_id: int) -> List[models.TrainingFeedback]:
    """Obtener feedback específico de una actividad"""
    return db.query(models.TrainingFeedback).filter(
        models.TrainingFeedback.activity_id == activity_id
    ).order_by(models.TrainingFeedback.created_at.desc()).all()


def create_training_feedback(db: Session, feedback: schemas.TrainingFeedbackCreate) -> models.TrainingFeedback:
    """Crear nuevo feedback de entrenamiento"""
    db_feedback = models.TrainingFeedback(**feedback.dict())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback


def update_training_feedback(db: Session, feedback_id: int, feedback_update: schemas.TrainingFeedbackUpdate) -> Optional[models.TrainingFeedback]:
    """Actualizar feedback de entrenamiento"""
    db_feedback = get_training_feedback(db, feedback_id)
    if db_feedback:
        update_data = feedback_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_feedback, field, value)
        db.commit()
        db.refresh(db_feedback)
    return db_feedback


def delete_training_feedback(db: Session, feedback_id: int) -> bool:
    """Eliminar feedback de entrenamiento"""
    db_feedback = get_training_feedback(db, feedback_id)
    if db_feedback:
        db.delete(db_feedback)
        db.commit()
        return True
    return False


# Funciones de estadísticas y resúmenes
def get_student_goal_summary(db: Session, student_id: int) -> dict:
    """Obtener resumen de objetivos del estudiante"""
    goals = get_student_goals(db, student_id, limit=1000)
    
    summary = {
        "total_goals": len(goals),
        "pending": len([g for g in goals if g.status == models.GoalStatus.PENDING]),
        "in_progress": len([g for g in goals if g.status == models.GoalStatus.IN_PROGRESS]),
        "completed": len([g for g in goals if g.status == models.GoalStatus.COMPLETED]),
        "cancelled": len([g for g in goals if g.status == models.GoalStatus.CANCELLED]),
        "completion_rate": 0
    }
    
    if summary["total_goals"] > 0:
        summary["completion_rate"] = (summary["completed"] / summary["total_goals"]) * 100
    
    return summary


def get_coach_activity_summary(db: Session, coach_id: int) -> dict:
    """Obtener resumen de actividad del entrenador"""
    goals = get_coach_goals(db, coach_id, limit=1000)
    feedback = get_coach_feedback(db, coach_id, limit=1000)
    
    return {
        "total_goals_created": len(goals),
        "total_feedback_given": len(feedback),
        "active_goals": len([g for g in goals if g.status == models.GoalStatus.IN_PROGRESS]),
        "completed_goals": len([g for g in goals if g.status == models.GoalStatus.COMPLETED])
    }