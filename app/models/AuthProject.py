from pydantic import BaseModel, validator


class AuthProject(BaseModel):
    project_id: str
    password: str