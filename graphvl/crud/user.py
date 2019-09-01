#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid

from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from graphvl.db_models.models import User
from graphvl.models.user import UserCreate


def get(db_session: Session, *, user_id: int) -> Optional[User]:
    return db_session.query(User).filter(User.user_id == user_id).first()


def get_multi(db_session: Session, *, skip=0, limit=100) -> List[Optional[User]]:
    return db_session.query(User).offset(skip).limit(limit).all()


def create(db_session: Session, *, user_in: UserCreate) -> User:
    user = User(
        user_id=user_in.user_id,
        name=user_in.name,
        surname=user_in.surname,
        date_of_birth=user_in.date_of_birth,
        country=user_in.country
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user
