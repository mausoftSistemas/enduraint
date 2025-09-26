from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from session.security import get_user_id_from_access_token
from . import crud, schemas, models
from users.user import crud as user_crud

router = APIRouter()


@router.get("/my-roles", response_model=List[schemas.UserRole])
def get_my_roles(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_user_id_from_access_token)
):
    """Obtiene los roles del usuario actual"""
    return crud.get_user_roles(db, current_user_id)


@router.get("/check-role/{role_type}", response_model=schemas.RoleCheckResponse)
def check_my_role(
    role_type: schemas.RoleTypeEnum,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_user_id_from_access_token)
):
    """Verifica si el usuario actual tiene un rol específico"""
    role = crud.get_user_role_by_type(db, current_user_id, models.RoleType(role_type))
    
    if role:
        return schemas.RoleCheckResponse(
            has_role=True,
            role_type=role_type,
            is_active=role.is_active,
            expires_at=role.expires_at
        )
    else:
        return schemas.RoleCheckResponse(has_role=False)


@router.post("/assign-role", response_model=schemas.UserRole)
def assign_role(
    role_request: schemas.RoleAssignmentRequest,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_user_id_from_access_token)
):
    """Asigna un rol a un usuario (solo administradores)"""
    # Verificar que el usuario actual es administrador
    if not crud.has_role(db, current_user_id, models.RoleType.ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden asignar roles"
        )
    
    # Verificar que el usuario objetivo existe
    target_user = user_crud.get_user_by_id(db, role_request.user_id)
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    try:
        role_create = schemas.UserRoleCreate(
            user_id=role_request.user_id,
            role_type=role_request.role_type,
            expires_at=role_request.expires_at,
            assigned_by=current_user_id
        )
        return crud.create_user_role(db, role_create, current_user_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/revoke-role/{user_id}/{role_type}")
def revoke_role(
    user_id: int,
    role_type: schemas.RoleTypeEnum,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_user_id_from_access_token)
):
    """Revoca un rol de un usuario (solo administradores)"""
    # Verificar que el usuario actual es administrador
    if not crud.has_role(db, current_user_id, models.RoleType.ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden revocar roles"
        )
    
    success = crud.deactivate_user_role(db, user_id, models.RoleType(role_type))
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado o ya inactivo"
        )
    
    return {"message": "Rol revocado exitosamente"}


@router.get("/users-by-role/{role_type}", response_model=List[schemas.UserWithRoles])
def get_users_by_role(
    role_type: schemas.RoleTypeEnum,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_user_id_from_access_token)
):
    """Obtiene todos los usuarios con un rol específico (solo administradores)"""
    # Verificar que el usuario actual es administrador
    if not crud.has_role(db, current_user_id, models.RoleType.ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden ver usuarios por rol"
        )
    
    users = crud.get_users_by_role(db, models.RoleType(role_type))
    return users


@router.get("/permissions/{role_type}", response_model=List[schemas.RolePermission])
def get_role_permissions(
    role_type: schemas.RoleTypeEnum,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_user_id_from_access_token)
):
    """Obtiene los permisos de un rol específico"""
    # Verificar que el usuario tiene el rol o es administrador
    if not (crud.has_role(db, current_user_id, models.RoleType(role_type)) or 
            crud.has_role(db, current_user_id, models.RoleType.ADMIN)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver los permisos de este rol"
        )
    
    return crud.get_role_permissions(db, models.RoleType(role_type))


@router.post("/initialize-permissions")
def initialize_permissions(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_user_id_from_access_token)
):
    """Inicializa los permisos por defecto (solo administradores)"""
    # Verificar que el usuario actual es administrador
    if not crud.has_role(db, current_user_id, models.RoleType.ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden inicializar permisos"
        )
    
    crud.initialize_default_permissions(db)
    return {"message": "Permisos inicializados exitosamente"}


@router.get("/check-permission/{permission}/{resource}")
def check_permission(
    permission: str,
    resource: str,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_user_id_from_access_token)
):
    """Verifica si el usuario actual tiene un permiso específico"""
    has_perm = crud.has_permission(db, current_user_id, permission, resource)
    return {"has_permission": has_perm}