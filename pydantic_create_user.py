from pydantic import BaseModel, EmailStr, Field, UUID4


class CreateUserRequestSchema(BaseModel):
    """Схема тела запроса для создания пользователя."""
    email: EmailStr = Field(max_length=250)
    password: str = Field(min_length=1, max_length=250)
    last_name: str = Field(alias='lastName', min_length=1, max_length=50)
    first_name: str = Field(alias='firstName', min_length=1, max_length=50)
    middle_name: str = Field(alias='middleName', min_length=1, max_length=50)


class UserSchema(BaseModel):
    """Схема данных пользователя, возвращаемая в ответе."""
    id: UUID4
    email: EmailStr = Field(max_length=250)
    last_name: str = Field(alias='lastName', min_length=1, max_length=50)
    first_name: str = Field(alias='firstName', min_length=1, max_length=50)
    middle_name: str = Field(alias='middleName', min_length=1, max_length=50)


class CreateUserResponseSchema(BaseModel):
    """Схема тела ответа после создания пользователя."""
    user: UserSchema
