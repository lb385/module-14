from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional

class UserRegisterSchema(BaseModel):
    """Schema for user registration."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=120)
    password: str = Field(..., min_length=8, max_length=255)
    confirm_password: Optional[str] = Field(None, max_length=255)

    @validator('username')
    def validate_username(cls, v):
        """Validate username contains only alphanumeric and underscore."""
        if not v.replace('_', '').isalnum():
            raise ValueError('Username must contain only alphanumeric characters and underscores')
        return v

    @validator('confirm_password', always=True)
    def passwords_match(cls, v, values):
        """Ensure password and confirm_password match."""
        if 'password' in values and v:
            if v != values['password']:
                raise ValueError('Passwords do not match')
        return v

    class Config:
        from_attributes = True

class UserLoginSchema(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str = Field(..., min_length=8)

    class Config:
        from_attributes = True

class UserResponseSchema(BaseModel):
    """Schema for user response."""
    id: int
    email: str
    username: str
    created_at: str

    class Config:
        from_attributes = True

class TokenResponseSchema(BaseModel):
    """Schema for token response."""
    access_token: str
    token_type: str
    user: UserResponseSchema
