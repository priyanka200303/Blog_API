from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    name: str


class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class ArticleCreate(BaseModel):
    title: str
    content: str
    category_id: int


class ArticleResponse(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    category_id: int

    class Config:
        from_attributes = True


class CommentCreate(BaseModel):
    text: str
    article_id: int


class CommentResponse(BaseModel):
    id: int
    text: str
    article_id: int
    user_id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None