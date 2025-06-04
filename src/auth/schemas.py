from typing import Self

from pydantic import BaseModel, EmailStr, model_validator, Field

class SUserAdd(BaseModel):
    username:str = Field(max_length=50)
    email:EmailStr = Field(max_length=128)
    password:str
    active:bool

class SUser(SUserAdd):
    id:int

class SUserRegister(BaseModel):
    email:EmailStr = Field(max_length=128)
    username:str = Field(max_length=50) 
    password:str
    password2:str

    @model_validator(mode="after")
    def check_passwords(self) -> Self:
        if self.password != self.password2:
            raise ValueError("Passwords do not match")
        return self 

class SUserLogin(BaseModel):
    email:EmailStr
    password:str