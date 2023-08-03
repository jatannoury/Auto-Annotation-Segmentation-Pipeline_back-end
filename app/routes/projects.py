import datetime

from fastapi import  APIRouter,HTTPException

from models.AuthProject import AuthProject
from models.Project import Project
from tools.dynamoDB import DynamoDbHandler


dynamoDB_handler = DynamoDbHandler()
router = APIRouter()

@router.post("/create", status_code=201)
def create_project(formData: Project):
    try:
        project_id = dynamoDB_handler.create_project(formData)
        return {"message": "Project created successfully!", "project_id":project_id}
    except:
        raise HTTPException(status_code=400)

@router.post("/authenticate", status_code=200)
def authenticate_project(formData: AuthProject):
    request_info = formData.__dict__
    db_response = dynamoDB_handler.get_table_info(request_info['project_id'])
    try:
        pass_verification = dynamoDB_handler.verify_password(request_info['password'],
                                                             db_response['Items'][0]['password'])
        if pass_verification:
            return {"message": "Correct credentials"}
        else:
            raise HTTPException(status_code=401)
    except:
        raise HTTPException(status_code=401)




