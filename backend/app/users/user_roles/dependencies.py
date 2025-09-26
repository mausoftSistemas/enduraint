from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Union

from core.database import get_db
from session.security import get_user_id_from_access_token
from . import crud, models


def require_role(required_role: Union[models.RoleType, List[models.RoleType]]):
    """Dependencia para requerir un rol específico o una lista de roles"""
    def check_role(
        db: Session = Depends(get_db),
        current_user_id: int = Depends(get_user_id_from_access_token)
    ):
        if isinstance(required_role, list):
            if not crud.has_any_role(db, current_user_id, required_role):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Se requiere uno de los siguientes roles: {[role.value for role in required_role]}"
                )
        else:
            if not crud.has_role(db, current_user_id, required_role):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Se requiere el rol: {required_role.value}"
                )
        return current_user_id
    
    return check_role


def require_coach_role():
    """Dependencia para requerir rol de entrenador"""
    return require_role(models.RoleType.COACH)


def require_student_role():
    """Dependencia para requerir rol de alumno"""
    return require_role(models.RoleType.STUDENT)


def require_admin_role():
    """Dependencia para requerir rol de administrador"""
    return require_role(models.RoleType.ADMIN)


def require_coach_or_admin():
    """Dependencia para requerir rol de entrenador o administrador"""
    return require_role([models.RoleType.COACH, models.RoleType.ADMIN])


def require_student_or_coach():
    """Dependencia para requerir rol de alumno o entrenador"""
    return require_role([models.RoleType.STUDENT, models.RoleType.COACH])


def require_permission(permission: str, resource: str):
    """Dependencia para requerir un permiso específico"""
    def check_permission(
        db: Session = Depends(get_db),
        current_user_id: int = Depends(get_user_id_from_access_token)
    ):
        if not crud.has_permission(db, current_user_id, permission, resource):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"No tienes permiso '{permission}' para el recurso '{resource}'"
            )
        return current_user_id
    
    return check_permission


def get_current_user_roles(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_user_id_from_access_token)
) -> List[models.UserRole]:
    """Obtiene los roles del usuario actual"""
    return crud.get_user_roles(db, current_user_id)


def is_coach_or_admin(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_user_id_from_access_token)
) -> bool:
    """Verifica si el usuario es entrenador o administrador"""
    return crud.has_any_role(db, current_user_id, [models.RoleType.COACH, models.RoleType.ADMIN])


def is_student_or_coach(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_user_id_from_access_token)
) -> bool:
    """Verifica si el usuario es alumno o entrenador"""
    return crud.has_any_role(db, current_user_id, [models.RoleType.STUDENT, models.RoleType.COACH])


def verify_coach_student_access(
    student_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_user_id_from_access_token)
):
    """Verifica que un entrenador tenga acceso a un alumno específico o que sea el propio alumno"""
    # Si es el propio alumno
    if current_user_id == student_id:
        return current_user_id
    
    # Si es administrador, tiene acceso total
    if crud.has_role(db, current_user_id, models.RoleType.ADMIN):
        return current_user_id
    
    # Si es entrenador, verificar que tenga al alumno asignado
    if crud.has_role(db, current_user_id, models.RoleType.COACH):
        from coaches import crud as coach_crud
        coach_student = coach_crud.get_coach_student_relationship(db, current_user_id, student_id)
        if coach_student and coach_student.is_active:
            return current_user_id
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="No tienes acceso a este alumno"
    )


def verify_student_coach_access(
    coach_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_user_id_from_access_token)
):
    """Verifica que un alumno tenga acceso a un entrenador específico o que sea el propio entrenador"""
    # Si es el propio entrenador
    if current_user_id == coach_id:
        return current_user_id
    
    # Si es administrador, tiene acceso total
    if crud.has_role(db, current_user_id, models.RoleType.ADMIN):
        return current_user_id
    
    # Si es alumno, verificar que tenga al entrenador asignado
    if crud.has_role(db, current_user_id, models.RoleType.STUDENT):
        from coaches import crud as coach_crud
        coach_student = coach_crud.get_coach_student_relationship(db, coach_id, current_user_id)
        if coach_student and coach_student.is_active:
            return current_user_id
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="No tienes acceso a este entrenador"
    )