from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from enum import Enum


class RoleTypeEnum(str, Enum):
    """Enum para los tipos de roles"""
    USER = "user"
    COACH = "coach"
    STUDENT = "student"
    ADMIN = "admin"


class UserRoleBase(BaseModel):
    """Esquema base para roles de usuario"""
    role_type: RoleTypeEnum
    is_active: bool = True
    expires_at: Optional[datetime] = None


class UserRoleCreate(UserRoleBase):
    """Esquema para crear un rol de usuario"""
    user_id: int
    assigned_by: Optional[int] = None


class UserRoleUpdate(BaseModel):
    """Esquema para actualizar un rol de usuario"""
    is_active: Optional[bool] = None
    expires_at: Optional[datetime] = None


class UserRole(UserRoleBase):
    """Esquema completo para rol de usuario"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    assigned_at: datetime
    assigned_by: Optional[int] = None


class RolePermissionBase(BaseModel):
    """Esquema base para permisos de rol"""
    role_type: RoleTypeEnum
    permission: str
    resource: str
    is_active: bool = True


class RolePermissionCreate(RolePermissionBase):
    """Esquema para crear un permiso de rol"""
    pass


class RolePermission(RolePermissionBase):
    """Esquema completo para permiso de rol"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime


class UserWithRoles(BaseModel):
    """Esquema para usuario con sus roles"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    username: str
    email: str
    name: str
    is_active: int
    user_roles: List[UserRole] = []


class RoleAssignmentRequest(BaseModel):
    """Esquema para solicitud de asignación de rol"""
    user_id: int
    role_type: RoleTypeEnum
    expires_at: Optional[datetime] = None


class RoleCheckResponse(BaseModel):
    """Esquema para respuesta de verificación de rol"""
    has_role: bool
    role_type: Optional[RoleTypeEnum] = None
    is_active: bool = False
    expires_at: Optional[datetime] = None