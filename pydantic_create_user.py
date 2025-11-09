from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    """Схема с данными для создания пользователя."""
    email: EmailStr
    password: str
    last_name: str = Field(alias='lastName')
    first_name: str = Field(alias='firstName')
    middle_name: str = Field(alias='middleName')


class UserResponseSchema(BaseModel):
    """Схема для данных пользователя в ответе."""
    id: str
    email: EmailStr
    last_name: str = Field(alias='lastName')
    first_name: str = Field(alias='firstName')
    middle_name: str = Field(alias='middleName')


class CreateUserRequestSchema(BaseModel):
    """Схема тела запроса для создания пользователя."""
    user: UserSchema


class CreateUserResponseSchema(BaseModel):
    """Схема тела ответа после создания пользователя."""
    user: UserResponseSchema
