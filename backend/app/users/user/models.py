from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Boolean,
    DateTime
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database_sqlite import Base


# Data model for users table using SQLAlchemy's ORM
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(
        String(length=250),
        nullable=False,
        comment="User real name (May include spaces)",
    )
    username = Column(
        String(length=250),
        nullable=False,
        unique=True,
        index=True,
        comment="User username (letters, numbers, and dots allowed)",
    )
    email = Column(
        String(length=250),
        nullable=False,
        unique=True,
        index=True,
        comment="User email (max 250 characters)",
    )
    password = Column(
        String(length=250), nullable=False, comment="User password (hash)"
    )
    city = Column(String(length=250), nullable=True, comment="User city")
    birthdate = Column(Date, nullable=True, comment="User birthdate (date)")
    preferred_language = Column(
        String(length=5),
        nullable=False,
        comment="User preferred language (en, pt, others)",
    )
    gender = Column(
        Integer,
        nullable=False,
        default=1,
        comment="User gender (one digit)(1 - male, 2 - female, 3 - unspecified)",
    )
    units = Column(
        Integer,
        nullable=False,
        default=1,
        comment="User units (one digit)(1 - metric, 2 - imperial)",
    )
    height = Column(Integer, nullable=True, comment="User height in centimeters")
    access_type = Column(
        Integer, nullable=False, comment="User type (one digit)(1 - user, 2 - admin)"
    )
    photo_path = Column(String(length=250), nullable=True, comment="User photo path")
    is_active = Column(
        Integer, nullable=False, comment="Is user active (1 - active, 2 - not active)"
    )
    first_day_of_week = Column(
        Integer,
        nullable=False,
        default=1,
        comment="User first day of week (0 - Sunday, 1 - Monday, etc.)",
    )
    currency = Column(
        Integer,
        nullable=False,
        default=1,
        comment="User currency (one digit)(1 - euro, 2 - dollar, 3 - pound)",
    )
    mfa_enabled = Column(
        Boolean,
        nullable=False,
        default=False,
        comment="Whether MFA is enabled for this user",
    )
    mfa_secret = Column(
        String(length=512),
        nullable=True,
        comment="User MFA secret for TOTP generation (encrypted at rest)",
    )

    # Relaciones para el sistema entrenador-alumno
    user_roles = relationship(
        "UserRole",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    coach_profile = relationship(
        "Coach",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    
    student_profile = relationship(
        "Student",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
