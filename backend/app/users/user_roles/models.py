from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database_sqlite import Base
import enum


class RoleType(enum.Enum):
    """Enum para los tipos de roles disponibles"""
    USER = "user"  # Usuario regular
    COACH = "coach"  # Entrenador
    STUDENT = "student"  # Alumno
    ADMIN = "admin"  # Administrador


class UserRole(Base):
    """Modelo para los roles de usuario"""
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, 
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False,
        comment="ID del usuario"
    )
    role_type = Column(
        Enum(RoleType), 
        nullable=False,
        comment="Tipo de rol del usuario"
    )
    is_active = Column(
        Boolean, 
        default=True, 
        nullable=False,
        comment="Si el rol está activo"
    )
    assigned_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(),
        comment="Fecha de asignación del rol"
    )
    assigned_by = Column(
        Integer, 
        ForeignKey("users.id"), 
        nullable=True,
        comment="ID del usuario que asignó el rol"
    )
    expires_at = Column(
        DateTime(timezone=True), 
        nullable=True,
        comment="Fecha de expiración del rol (opcional)"
    )
    
    # Relaciones
    user = relationship(
        "User", 
        back_populates="user_roles",
        foreign_keys=[user_id]
    )
    assigned_by_user = relationship(
        "User", 
        foreign_keys=[assigned_by]
    )

    def __repr__(self):
        return f"<UserRole(user_id={self.user_id}, role={self.role_type.value})>"


class RolePermission(Base):
    """Modelo para los permisos asociados a roles"""
    __tablename__ = "role_permissions"

    id = Column(Integer, primary_key=True, index=True)
    role_type = Column(
        Enum(RoleType), 
        nullable=False,
        comment="Tipo de rol"
    )
    permission = Column(
        String(100), 
        nullable=False,
        comment="Nombre del permiso"
    )
    resource = Column(
        String(100), 
        nullable=False,
        comment="Recurso al que aplica el permiso"
    )
    is_active = Column(
        Boolean, 
        default=True, 
        nullable=False,
        comment="Si el permiso está activo"
    )
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(),
        comment="Fecha de creación del permiso"
    )

    def __repr__(self):
        return f"<RolePermission(role={self.role_type.value}, permission={self.permission}, resource={self.resource})>"