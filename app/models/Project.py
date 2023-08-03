from pydantic import BaseModel, validator


class Project(BaseModel):
    project_name: str
    total_images: int
    password: str
    user_id:str