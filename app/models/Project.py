from pydantic import BaseModel, validator


class Project(BaseModel):
    projectName: str
    totalNumber: int
    password: str
    userId:str
    protect:bool
    createdAt:str = None