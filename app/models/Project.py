from pydantic import BaseModel, validator


class Project(BaseModel):
    projectName: str
    storageType: str
    password: str
    userId:str
    protect:bool
    createdAt:str = None