import datetime
import os

import boto3
from fastapi.exceptions import HTTPException
import uuid
from passlib.context import CryptContext
from dotenv import load_dotenv

from models.AuthProject import AuthProject
from models.Project import Project
from models.RunningProject import RunningProject
from models.User import User
import requests
from config.lambda_functions_URLs import RUN_PROJECT_ORCHESTRATOR_URL

load_dotenv()


class DynamoDbHandler:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        dynamo_db_client = boto3.resource(
            'dynamodb',
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
        )
        self.users_table = dynamo_db_client.Table("users")
        self.projects_table = dynamo_db_client.Table("projects")
        self.running_projects_table = dynamo_db_client.Table("running_projects")

    # Password encryption function
    def encrypt_password(self, password: str) -> str:
        encrypted_pass = self.pwd_context.hash(password)
        return encrypted_pass

    def verify_password(self, password: str, hashed_password: str) -> bool:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(password, hashed_password)

    def post_user_table(self, user_data:User) -> str:
        try:
            user_data = user_data.__dict__
            user_data['userId'] = str(uuid.uuid4())
            user_data['password'] = self.encrypt_password(user_data['password'])
            self.users_table.put_item(Item=user_data)
            return "Created"
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def get_user_info(self, user_email) -> str:
        try:
            filter_expression = 'email = :user_email'
            expression_attribute_values = {
                ":user_email": user_email
            }
            return self.users_table.scan(
                FilterExpression=filter_expression,
                ExpressionAttributeValues=expression_attribute_values
            )


        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def create_project(self,project_info:Project):
        try:
            project_info = project_info.__dict__
            project_info['project_id'] = str(uuid.uuid4())
            project_info['createdAt'] = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            project_info['status'] = "Pending"
            if project_info['password'] != "" or project_info['password'] != None:
                project_info['password'] = self.encrypt_password(project_info['password'])
            self.projects_table.put_item(Item=project_info)
            return project_info
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def get_table_info(self,project_id):
        filter_expression = 'project_id = :id'
        expression_attribute_values = {
            ":id": project_id
        }
        return self.projects_table.scan(
            FilterExpression=filter_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
    def get_projects_by_user_id(self,user_id:str):
        try:
            print(user_id)
            filter_expression = 'userId = :user_id'
            expression_attribute_values = {
                ":user_id": user_id
            }
            return self.projects_table.scan(
                FilterExpression=filter_expression,
                ExpressionAttributeValues=expression_attribute_values
            )


        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
    def delete_project(self,project_id:str):
        try:
            response = self.projects_table.delete_item(
                Key={
                    "project_id": project_id
                }
            )
            return response
        except:
            raise HTTPException(status_code=500,detail="Internal Server Error")

    async def create_running_project(self,project_info:RunningProject):
        try:
            project_info = project_info.__dict__
            print(project_info)
            project_info['created_at'] = f"{datetime.datetime.utcnow()}"
            project_info['finished_at'] = ""
            self.running_projects_table.put_item(Item=project_info)
            created_instance_id = requests.post(f"{RUN_PROJECT_ORCHESTRATOR_URL}?project_name={project_info['project_name']}&user_id={project_info['userId']}")
            # project_info['created_instance_id'] = created_instance_id.text
            return project_info['project_id']
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")


if __name__ == "__main__":
    dynamoDB_handler = DynamoDbHandler()
    user_test_info = {
        "firstName":"John",
        "lastName":"Doe",
        "birthday":"17-04-2000",
        "gender":"Male",
        "email":"johnDoe@outlook.com",
        "password":"123456",
    }
    user_object = User(**user_test_info)
    # dynamoDB_handler.post_user_table(user_object)
    response = dynamoDB_handler.get_user_info(user_test_info['email'])
    print(response)



