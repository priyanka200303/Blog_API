from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.oauth2 import get_current_user

router = APIRouter(
    prefix="/articles",
    tags=["Articles"]
)


@router.post(
    "/",
    response_model=schemas.ArticleResponse
)
def create_article(
    article: schemas.ArticleCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    new_article = models.Article(
        title=article.title,
        content=article.content,
        category_id=article.category_id,
        user_id=current_user.id
    )

    db.add(new_article)
    db.commit()
    db.refresh(new_article)

    return new_article


@router.get(
    "/",
    response_model=list[schemas.ArticleResponse]
)
def get_articles(
    db: Session = Depends(get_db)
):
    articles = db.query(
        models.Article
    ).all()

    return articles


@router.get(
    "/{article_id}",
    response_model=schemas.ArticleResponse
)
def get_single_article(
    article_id: int,
    db: Session = Depends(get_db)
):
    article = db.query(models.Article).filter(
        models.Article.id == article_id
    ).first()

    if not article:
        raise HTTPException(
            status_code=404,
            detail="Article not found"
        )

    return article


@router.put(
    "/{article_id}",
    response_model=schemas.ArticleResponse
)
def update_article(
    article_id: int,
    updated_article: schemas.ArticleCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    article = db.query(models.Article).filter(
        models.Article.id == article_id
    ).first()

    if not article:
        raise HTTPException(
            status_code=404,
            detail="Article not found"
        )

    if article.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    article.title = updated_article.title
    article.content = updated_article.content
    article.category_id = updated_article.category_id

    db.commit()
    db.refresh(article)

    return article


@router.delete(
    "/{article_id}"
)
def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    article = db.query(models.Article).filter(
        models.Article.id == article_id
    ).first()

    if not article:
        raise HTTPException(
            status_code=404,
            detail="Article not found"
        )

    if article.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    db.delete(article)
    db.commit()

    return {"message": "Article deleted successfully"}