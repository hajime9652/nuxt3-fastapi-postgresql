from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

import uuid
from app.db.base_class import Base

class User(Base):
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    
    # basic information
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # user information
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    is_onboarding = Column(Boolean(), default=False)
    is_email_validation = Column(Boolean(), default=False)
