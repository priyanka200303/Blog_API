from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.oauth2 import get_current_user

router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)


@router.post(
    "/",
    response_model=schemas.CommentResponse
)
def create_comment(
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    new_comment = models.Comment(
        text=comment.text,
        article_id=comment.article_id,
        user_id=current_user.id
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment


@router.get(
    "/{article_id}",
    response_model=list[schemas.CommentResponse]
)
def get_comments(
    article_id: int,
    db: Session = Depends(get_db)
):
    comments = db.query(models.Comment).filter(
        models.Comment.article_id == article_id
    ).all()

    return comments