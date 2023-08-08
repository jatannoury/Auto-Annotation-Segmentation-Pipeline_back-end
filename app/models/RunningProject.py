from pydantic import BaseModel
class RunningProject(BaseModel):
    nb_of_files: int
    newest: str
    oldest: str
    total_size_GB: str
    total_size_MB: str
    projectName:str
    project_id:str
    protect:bool
    status:str
    storageType:str
    total_size_GB:str
    total_size_MB:str
    userId:str
    s3_trainig_path:str
    project_name:str