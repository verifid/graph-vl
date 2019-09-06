#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from graphvl.db_models.models import Image
from graphvl.models.image import ImageCreate

def get(db_session: Session, *, user_id: int) -> Optional[Image]:
    return db_session.query(Image).filter(Image.user_id == user_id).first()


def create(db_session: Session, *, image_in: ImageCreate) -> ImageCreate:
    image = Image(
        image_id=image_in.image_id,
        user_id=image_in.user_id,
        image_str=image_in.image_str,
        image_type=image_in.image_type
    )
    db_session.add(image)
    db_session.commit()
    db_session.refresh(image)
    return image
