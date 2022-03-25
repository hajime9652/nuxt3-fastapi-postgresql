from logging import root
from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.utils import send_new_account_email, send_invite_account_email, generate_email_valid_token

import uuid
from uuid import UUID

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users

@router.post("/", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    if settings.EMAILS_ENABLED and user_in.email:
        email_valid_token = generate_email_valid_token(email=user_in.email)
        send_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password, token=email_valid_token
        )
    return user


@router.put("/me", response_model=schemas.User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(None),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
        
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/me", response_model=schemas.User)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.post("/open", response_model=schemas.User)
def create_user_open(
    *,
    db: Session = Depends(deps.get_db),
    email: EmailStr = Body(..., embed=True),
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = crud.user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    password = str(uuid.uuid4())[:8]
    full_name = email.split('@')[0]
    user_in = schemas.UserCreate(
        password=password,
        email=email,
        full_name=full_name,
        is_email_validation=False,
        is_onboarding=True,
        )
    user = crud.user.create(db, obj_in=user_in)

    email_valid_token = generate_email_valid_token(email=email)
    if settings.EMAILS_ENABLED:
        send_new_account_email(
            email_to=user_in.email, username=user_in.full_name, password=password, token=email_valid_token
        )
    return user


@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(
    user_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud.user.get(db, id=user_id)
    if user == current_user:
        return user
    return user

@router.get("/{user_id}/deactivate", response_model=schemas.User)
def deactivate_user(
    user_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Deactivate a user by id.
    """
    if not user_id in [member.id for room in current_user.rooms for member in room.members]:
        raise HTTPException(
            status_code=400,
            detail="The user doesn't have enough privilege",
        )
    user = crud.user.get(db, id=user_id)
    user.is_active = False
    db.add(user)
    db.commit()
    
    return user

@router.get("/{user_id}/activate", response_model=schemas.User)
def deactivate_user(
    user_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Activate a user by id.
    """
    if not user_id in [member.id for room in current_user.rooms for member in room.members]:
        raise HTTPException(
            status_code=400,
            detail="The user doesn't have enough privilege",
        )
    user = crud.user.get(db, id=user_id)
    user.is_active = True
    db.add(user)
    db.commit()
    
    return user

@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: UUID,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user
