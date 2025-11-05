from typing import Annotated, Optional, List
from annotated_types import Ge, Le
from pydantic import BaseModel, EmailStr, ConfigDict, StringConstraints

# Type aliases
NameStr = Annotated[str, StringConstraints(min_length=1, max_length=100)]
StudentIdStr = Annotated[str, StringConstraints(pattern=r"^S\d{7}$")]
CodeStr = Annotated[str, StringConstraints(min_length=1, max_length=32)]
CourseNameStr = Annotated[str, StringConstraints(min_length=1, max_length=255)]
ProjectNameStr = Annotated[str, StringConstraints(min_length=1, max_length=255)]
DescStr = Annotated[str, StringConstraints(min_length=0, max_length=2000)]
AgeInt = Annotated[int, Ge(0), Le(150)]
CreditsInt = Annotated[int, Ge(1), Le(120)]

# Users
class UserCreate(BaseModel):
    name: NameStr
    email: EmailStr
    age: AgeInt
    student_id: StudentIdStr

class UserUpdate(BaseModel):
    name: Optional[NameStr] = None
    email: Optional[EmailStr] = None
    age: Optional[AgeInt] = None
    student_id: Optional[StudentIdStr] = None

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: NameStr
    email: EmailStr
    age: AgeInt
    student_id: StudentIdStr

class ProjectRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: ProjectNameStr
    description: Optional[DescStr] = None
    owner_id: int

class UserReadWithProjects(UserRead):
    projects: List[ProjectRead] = []

# Projects
class ProjectCreate(BaseModel):
    name: ProjectNameStr
    description: Optional[DescStr] = None
    owner_id: int

class ProjectUpdate(BaseModel):
    name: Optional[ProjectNameStr] = None
    description: Optional[DescStr] = None
    owner_id: Optional[int] = None

class ProjectCreateForUser(BaseModel):
    name: ProjectNameStr
    description: Optional[DescStr] = None

class ProjectReadWithOwner(ProjectRead):
    owner: Optional["UserRead"] = None

# Courses
class CourseCreate(BaseModel):
    code: CodeStr
    name: CourseNameStr
    credits: CreditsInt

class CourseRead(CourseCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int

