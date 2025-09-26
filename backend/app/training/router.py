from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from session.security import get_user_id_from_access_token
from users.user_roles.dependencies import require_coach_role, require_student_role, verify_coach_student_access
from . import crud, schemas

router = APIRouter(prefix="/training", tags=["training"])


# Endpoints para objetivos de entrenamiento
@router.post("/goals", response_model=schemas.TrainingGoal)
def create_training_goal(
    goal: schemas.TrainingGoalCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_user_id_from_access_token),
    _: bool = Depends(require_coach_role)
):
    """Crear nuevo objetivo de entrenamiento"""
    # Verificar que el usuario actual sea el entrenador
    from coaches.crud import get_coach
    coach = get_coach(db, goal.coach_id)
    if not coach or coach.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para crear objetivos para este entrenador"
        )
    
    # Verificar que el estudiante exista y esté asociado al entrenador
    from coaches.crud import get_coach_student_relationship
    relationship = get_coach_student_relationship(db, goal.coach_id, goal.student_id)
    if not relationship:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El estudiante no está asociado a este entrenador"
        )
    
    return crud.create_training_goal(db=db, goal=goal)


@router.get("/goals", response_model=List[schemas.TrainingGoal])
def read_training_goals(
    skip: int = 0,
    limit: int = 100,
    coach_id: int = None,
    student_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtener objetivos de entrenamiento"""
    if coach_id:
        # Verificar permisos para ver objetivos del entrenador
        from coaches.crud import get_coach
        coach = get_coach(db, coach_id)
        if not coach or coach.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para ver los objetivos de este entrenador"
            )
        return crud.get_coach_goals(db, coach_id, skip=skip, limit=limit)
    
    elif student_id:
        # Verificar permisos para ver objetivos del estudiante
        from students.crud import get_student
        student = get_student(db, student_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Estudiante no encontrado"
            )
        
        # El estudiante puede ver sus propios objetivos, o su entrenador
        if student.user_id != current_user.id:
            from coaches.crud import get_coach_by_user_id, get_coach_student_relationship
            coach = get_coach_by_user_id(db, current_user.id)
            if not coach or not get_coach_student_relationship(db, coach.id, student_id):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tienes permisos para ver los objetivos de este estudiante"
                )
        
        return crud.get_student_goals(db, student_id, skip=skip, limit=limit)
    
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe especificar coach_id o student_id"
        )


@router.get("/goals/me/coach", response_model=List[schemas.TrainingGoal])
def get_my_coach_goals(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtener objetivos creados por el entrenador actual"""
    from coaches.crud import get_coach_by_user_id
    coach = get_coach_by_user_id(db, current_user.id)
    if not coach:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entrenador no encontrado"
        )
    
    return crud.get_coach_goals(db, coach.id, skip=skip, limit=limit)


@router.get("/goals/me/student", response_model=List[schemas.TrainingGoal])
def get_my_student_goals(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtener objetivos asignados al estudiante actual"""
    from students.crud import get_student_by_user_id
    student = get_student_by_user_id(db, current_user.id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado"
        )
    
    return crud.get_student_goals(db, student.id, skip=skip, limit=limit)


@router.get("/goals/{goal_id}", response_model=schemas.TrainingGoalWithFeedback)
def read_training_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtener objetivo de entrenamiento por ID"""
    goal = crud.get_training_goal(db, goal_id=goal_id)
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Objetivo no encontrado"
        )
    
    # Verificar permisos
    from coaches.crud import get_coach
    from students.crud import get_student
    
    coach = get_coach(db, goal.coach_id)
    student = get_student(db, goal.student_id)
    
    if (coach and coach.user_id == current_user.id) or (student and student.user_id == current_user.id):
        return goal
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver este objetivo"
        )


@router.put("/goals/{goal_id}", response_model=schemas.TrainingGoal)
def update_training_goal(
    goal_id: int,
    goal_update: schemas.TrainingGoalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualizar objetivo de entrenamiento"""
    goal = crud.get_training_goal(db, goal_id)
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Objetivo no encontrado"
        )
    
    # Solo el entrenador puede actualizar el objetivo
    from coaches.crud import get_coach
    coach = get_coach(db, goal.coach_id)
    if not coach or coach.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el entrenador puede actualizar este objetivo"
        )
    
    return crud.update_training_goal(db=db, goal_id=goal_id, goal_update=goal_update)


@router.put("/goals/{goal_id}/progress", response_model=schemas.TrainingGoal)
def update_goal_progress(
    goal_id: int,
    progress: schemas.TrainingGoalProgress,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualizar progreso de objetivo"""
    goal = crud.get_training_goal(db, goal_id)
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Objetivo no encontrado"
        )
    
    # Tanto el entrenador como el estudiante pueden actualizar el progreso
    from coaches.crud import get_coach
    from students.crud import get_student
    
    coach = get_coach(db, goal.coach_id)
    student = get_student(db, goal.student_id)
    
    if not ((coach and coach.user_id == current_user.id) or (student and student.user_id == current_user.id)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para actualizar el progreso de este objetivo"
        )
    
    return crud.update_goal_progress(db=db, goal_id=goal_id, progress=progress)


@router.delete("/goals/{goal_id}")
def delete_training_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Eliminar objetivo de entrenamiento"""
    goal = crud.get_training_goal(db, goal_id)
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Objetivo no encontrado"
        )
    
    # Solo el entrenador puede eliminar el objetivo
    from coaches.crud import get_coach
    coach = get_coach(db, goal.coach_id)
    if not coach or coach.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el entrenador puede eliminar este objetivo"
        )
    
    success = crud.delete_training_goal(db=db, goal_id=goal_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo eliminar el objetivo"
        )
    
    return {"message": "Objetivo eliminado exitosamente"}


# Endpoints para feedback de entrenamiento
@router.post("/feedback", response_model=schemas.TrainingFeedback)
def create_training_feedback(
    feedback: schemas.TrainingFeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crear nuevo feedback de entrenamiento"""
    # Verificar que el usuario actual sea el entrenador
    from coaches.crud import get_coach
    coach = get_coach(db, feedback.coach_id)
    if not coach or coach.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para crear feedback para este entrenador"
        )
    
    # Verificar que el estudiante esté asociado al entrenador
    from coaches.crud import get_coach_student_relationship
    relationship = get_coach_student_relationship(db, feedback.coach_id, feedback.student_id)
    if not relationship:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El estudiante no está asociado a este entrenador"
        )
    
    return crud.create_training_feedback(db=db, feedback=feedback)


@router.get("/feedback", response_model=List[schemas.TrainingFeedback])
def read_training_feedback(
    skip: int = 0,
    limit: int = 100,
    coach_id: int = None,
    student_id: int = None,
    goal_id: int = None,
    activity_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtener feedback de entrenamiento"""
    if goal_id:
        return crud.get_goal_feedback(db, goal_id)
    elif activity_id:
        return crud.get_activity_feedback(db, activity_id)
    elif coach_id:
        # Verificar permisos
        from coaches.crud import get_coach
        coach = get_coach(db, coach_id)
        if not coach or coach.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para ver el feedback de este entrenador"
            )
        return crud.get_coach_feedback(db, coach_id, skip=skip, limit=limit)
    elif student_id:
        # Verificar permisos
        from students.crud import get_student
        student = get_student(db, student_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Estudiante no encontrado"
            )
        
        if student.user_id != current_user.id:
            from coaches.crud import get_coach_by_user_id, get_coach_student_relationship
            coach = get_coach_by_user_id(db, current_user.id)
            if not coach or not get_coach_student_relationship(db, coach.id, student_id):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tienes permisos para ver el feedback de este estudiante"
                )
        
        return crud.get_student_feedback(db, student_id, skip=skip, limit=limit)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe especificar al menos un filtro (coach_id, student_id, goal_id, activity_id)"
        )


@router.get("/feedback/me/given", response_model=List[schemas.TrainingFeedback])
def get_my_given_feedback(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtener feedback dado por el entrenador actual"""
    from coaches.crud import get_coach_by_user_id
    coach = get_coach_by_user_id(db, current_user.id)
    if not coach:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entrenador no encontrado"
        )
    
    return crud.get_coach_feedback(db, coach.id, skip=skip, limit=limit)


@router.get("/feedback/me/received", response_model=List[schemas.TrainingFeedback])
def get_my_received_feedback(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtener feedback recibido por el estudiante actual"""
    from students.crud import get_student_by_user_id
    student = get_student_by_user_id(db, current_user.id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado"
        )
    
    return crud.get_student_feedback(db, student.id, skip=skip, limit=limit)


@router.get("/feedback/{feedback_id}", response_model=schemas.TrainingFeedback)
def read_training_feedback_item(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtener feedback específico por ID"""
    feedback = crud.get_training_feedback(db, feedback_id)
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback no encontrado"
        )
    
    # Verificar permisos
    from coaches.crud import get_coach
    from students.crud import get_student
    
    coach = get_coach(db, feedback.coach_id)
    student = get_student(db, feedback.student_id)
    
    if not ((coach and coach.user_id == current_user.id) or (student and student.user_id == current_user.id)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver este feedback"
        )
    
    return feedback


@router.put("/feedback/{feedback_id}", response_model=schemas.TrainingFeedback)
def update_training_feedback(
    feedback_id: int,
    feedback_update: schemas.TrainingFeedbackUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualizar feedback de entrenamiento"""
    feedback = crud.get_training_feedback(db, feedback_id)
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback no encontrado"
        )
    
    # Solo el entrenador que creó el feedback puede actualizarlo
    from coaches.crud import get_coach
    coach = get_coach(db, feedback.coach_id)
    if not coach or coach.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el entrenador que creó el feedback puede actualizarlo"
        )
    
    return crud.update_training_feedback(db=db, feedback_id=feedback_id, feedback_update=feedback_update)


@router.delete("/feedback/{feedback_id}")
def delete_training_feedback(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Eliminar feedback de entrenamiento"""
    feedback = crud.get_training_feedback(db, feedback_id)
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback no encontrado"
        )
    
    # Solo el entrenador que creó el feedback puede eliminarlo
    from coaches.crud import get_coach
    coach = get_coach(db, feedback.coach_id)
    if not coach or coach.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el entrenador que creó el feedback puede eliminarlo"
        )
    
    success = crud.delete_training_feedback(db=db, feedback_id=feedback_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo eliminar el feedback"
        )
    
    return {"message": "Feedback eliminado exitosamente"}


# Endpoints de estadísticas y resúmenes
@router.get("/students/{student_id}/goals/summary")
def get_student_goal_summary(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtener resumen de objetivos del estudiante"""
    # Verificar permisos
    from students.crud import get_student
    student = get_student(db, student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante no encontrado"
        )
    
    if student.user_id != current_user.id:
        from coaches.crud import get_coach_by_user_id, get_coach_student_relationship
        coach = get_coach_by_user_id(db, current_user.id)
        if not coach or not get_coach_student_relationship(db, coach.id, student_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para ver el resumen de este estudiante"
            )
    
    return crud.get_student_goal_summary(db, student_id)


@router.get("/coaches/me/activity/summary")
def get_my_coach_activity_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtener resumen de actividad del entrenador actual"""
    from coaches.crud import get_coach_by_user_id
    coach = get_coach_by_user_id(db, current_user.id)
    if not coach:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entrenador no encontrado"
        )
    
    return crud.get_coach_activity_summary(db, coach.id)