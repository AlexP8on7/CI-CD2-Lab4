# app/schemas.py
from pydantic import BaseModel, EmailStr, constr, conint, field_validator
import re

class User(BaseModel):
 user_id: int
 name: constr(min_length=2, max_length=50)
 email: EmailStr
 age: conint(gt=18)
 student_id: constr(min_length=8, max_length=8, pattern='S[0-9]')
