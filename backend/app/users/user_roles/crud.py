from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime
from typing import List, Optional

from . import models, schemas
from users.user import models as user_models


def get_user_roles(db: Session, user_id: int, active_only: bool = True) -> List[models.UserRole]:
    """Obtiene todos los roles de un usuario"""
    query = db.query(models.UserRole).filter(models.UserRole.user_id == user_id)
    
    if active_only:
        query = query.filter(
            and_(
                models.UserRole.is_active == True,
                or_(
                    models.UserRole.expires_at.is_(None),
                    models.UserRole.expires_at > datetime.utcnow()
                )
            )
        )
    
    return query.all()


def get_user_role_by_type(db: Session, user_id: int, role_type: models.RoleType) -> Optional[models.UserRole]:
    """Obtiene un rol específico de un usuario"""
    return db.query(models.UserRole).filter(
        and_(
            models.UserRole.user_id == user_id,
            models.UserRole.role_type == role_type,
            models.UserRole.is_active == True,
            or_(
                models.UserRole.expires_at.is_(None),
                models.UserRole.expires_at > datetime.utcnow()
            )
        )
    ).first()


def has_role(db: Session, user_id: int, role_type: models.RoleType) -> bool:
    """Verifica si un usuario tiene un rol específico"""
    role = get_user_role_by_type(db, user_id, role_type)
    return role is not None


def has_any_role(db: Session, user_id: int, role_types: List[models.RoleType]) -> bool:
    """Verifica si un usuario tiene alguno de los roles especificados"""
    return db.query(models.UserRole).filter(
        and_(
            models.UserRole.user_id == user_id,
            models.UserRole.role_type.in_(role_types),
            models.UserRole.is_active == True,
            or_(
                models.UserRole.expires_at.is_(None),
                models.UserRole.expires_at > datetime.utcnow()
            )
        )
    ).first() is not None


def create_user_role(db: Session, role: schemas.UserRoleCreate, assigned_by: Optional[int] = None) -> models.UserRole:
    """Crea un nuevo rol para un usuario"""
    # Verificar si el usuario ya tiene este rol activo
    existing_role = get_user_role_by_type(db, role.user_id, models.RoleType(role.role_type))
    if existing_role:
        raise ValueError(f"El usuario ya tiene el rol {role.role_type}")
    
    db_role = models.UserRole(
        user_id=role.user_id,
        role_type=models.RoleType(role.role_type),
        is_active=role.is_active,
        expires_at=role.expires_at,
        assigned_by=assigned_by
    )
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def update_user_role(db: Session, role_id: int, role_update: schemas.UserRoleUpdate) -> Optional[models.UserRole]:
    """Actualiza un rol de usuario"""
    db_role = db.query(models.UserRole).filter(models.UserRole.id == role_id).first()
    if not db_role:
        return None
    
    update_data = role_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_role, field, value)
    
    db.commit()
    db.refresh(db_role)
    return db_role


def deactivate_user_role(db: Session, user_id: int, role_type: models.RoleType) -> bool:
    """Desactiva un rol específico de un usuario"""
    db_role = get_user_role_by_type(db, user_id, role_type)
    if not db_role:
        return False
    
    db_role.is_active = False
    db.commit()
    return True


def delete_user_role(db: Session, role_id: int) -> bool:
    """Elimina un rol de usuario"""
    db_role = db.query(models.UserRole).filter(models.UserRole.id == role_id).first()
    if not db_role:
        return False
    
    db.delete(db_role)
    db.commit()
    return True


def get_users_by_role(db: Session, role_type: models.RoleType, active_only: bool = True) -> List[user_models.User]:
    """Obtiene todos los usuarios que tienen un rol específico"""
    query = db.query(user_models.User).join(models.UserRole).filter(
        models.UserRole.role_type == role_type
    )
    
    if active_only:
        query = query.filter(
            and_(
                models.UserRole.is_active == True,
                or_(
                    models.UserRole.expires_at.is_(None),
                    models.UserRole.expires_at > datetime.utcnow()
                )
            )
        )
    
    return query.all()


def get_role_permissions(db: Session, role_type: models.RoleType) -> List[models.RolePermission]:
    """Obtiene todos los permisos de un rol"""
    return db.query(models.RolePermission).filter(
        and_(
            models.RolePermission.role_type == role_type,
            models.RolePermission.is_active == True
        )
    ).all()


def has_permission(db: Session, user_id: int, permission: str, resource: str) -> bool:
    """Verifica si un usuario tiene un permiso específico"""
    user_roles = get_user_roles(db, user_id)
    role_types = [role.role_type for role in user_roles]
    
    return db.query(models.RolePermission).filter(
        and_(
            models.RolePermission.role_type.in_(role_types),
            models.RolePermission.permission == permission,
            models.RolePermission.resource == resource,
            models.RolePermission.is_active == True
        )
    ).first() is not None


def create_role_permission(db: Session, permission: schemas.RolePermissionCreate) -> models.RolePermission:
    """Crea un nuevo permiso para un rol"""
    db_permission = models.RolePermission(
        role_type=models.RoleType(permission.role_type),
        permission=permission.permission,
        resource=permission.resource,
        is_active=permission.is_active
    )
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission


def initialize_default_permissions(db: Session):
    """Inicializa los permisos por defecto para cada rol"""
    default_permissions = [
        # Permisos para COACH
        {"role_type": models.RoleType.COACH, "permission": "read", "resource": "students"},
        {"role_type": models.RoleType.COACH, "permission": "write", "resource": "students"},
        {"role_type": models.RoleType.COACH, "permission": "read", "resource": "training_goals"},
        {"role_type": models.RoleType.COACH, "permission": "write", "resource": "training_goals"},
        {"role_type": models.RoleType.COACH, "permission": "read", "resource": "training_feedback"},
        {"role_type": models.RoleType.COACH, "permission": "write", "resource": "training_feedback"},
        
        # Permisos para STUDENT
        {"role_type": models.RoleType.STUDENT, "permission": "read", "resource": "own_profile"},
        {"role_type": models.RoleType.STUDENT, "permission": "write", "resource": "own_profile"},
        {"role_type": models.RoleType.STUDENT, "permission": "read", "resource": "own_training_goals"},
        {"role_type": models.RoleType.STUDENT, "permission": "read", "resource": "own_training_feedback"},
        {"role_type": models.RoleType.STUDENT, "permission": "write", "resource": "progress_records"},
        
        # Permisos para ADMIN
        {"role_type": models.RoleType.ADMIN, "permission": "read", "resource": "all"},
        {"role_type": models.RoleType.ADMIN, "permission": "write", "resource": "all"},
        {"role_type": models.RoleType.ADMIN, "permission": "delete", "resource": "all"},
    ]
    
    for perm_data in default_permissions:
        # Verificar si el permiso ya existe
        existing = db.query(models.RolePermission).filter(
            and_(
                models.RolePermission.role_type == perm_data["role_type"],
                models.RolePermission.permission == perm_data["permission"],
                models.RolePermission.resource == perm_data["resource"]
            )
        ).first()
        
        if not existing:
            db_permission = models.RolePermission(**perm_data)
            db.add(db_permission)
    
    db.commit()