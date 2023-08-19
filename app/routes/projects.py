import datetime
from typing import List, Dict
import httpx

import requests
from fastapi import APIRouter, HTTPException, Query, UploadFile
from pydantic import BaseModel

from config.lambda_functions_URLs import RUN_PROJECT_ORCHESTRATOR_URL
from models.AuthProject import AuthProject
from models.Project import Project
from models.RunningProject import RunningProject
from tools.dynamoDB import DynamoDbHandler


dynamoDB_handler = DynamoDbHandler()
router = APIRouter()

@router.post("/create", status_code=201)
def create_project(formData: Project):
    try:
        project_info = dynamoDB_handler.create_project(formData)
        return {"message": "Project created successfully!", "project_info":project_info}
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

@router.get("/projects", status_code=200)
def get_projects(user_id:str = Query(..., description="user_id")):
    try:
        db_response = dynamoDB_handler.get_projects_by_user_id(user_id)
        return {"items_count":db_response['Count'],"data":db_response['Items']}
    except:
        raise HTTPException(status_code=401)

@router.delete("/", status_code=200)
def delete_project(project_id:str = Query(..., description="project_id")):
    try:
        db_response = dynamoDB_handler.delete_project(project_id)
        return {"message":"Project Deleted","project_id":project_id}
    except:
        raise HTTPException(status_code=401)



@router.post("/start-project", status_code=201)
async def start_project(running_project: RunningProject):
    try:
        project_id = await dynamoDB_handler.create_running_project(running_project)
        print(project_id)
        return {"message": "Project Running", "project_id": project_id}
    except:
        raise HTTPException(status_code=500)
