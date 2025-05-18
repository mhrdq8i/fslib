from pydantic import BaseModel, constr


# Auth tokens

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Password reset


class PasswordResetRequest(BaseModel):
    email: str


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: constr(min_length=8)
