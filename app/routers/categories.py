from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.post(
    "/",
    response_model=schemas.CategoryResponse
)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db)
):
    new_category = models.Category(
        name=category.name
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


@router.get(
    "/",
    response_model=list[schemas.CategoryResponse]
)
def get_categories(
    db: Session = Depends(get_db)
):
    categories = db.query(
        models.Category
    ).all()

    return categories