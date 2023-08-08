from fastapi import  APIRouter,HTTPException,Response

from models.SignIn import SignIn
from models.User import User
from tools.dynamoDB import DynamoDbHandler


dynamoDB_handler = DynamoDbHandler()
router = APIRouter()

@router.post("/register", status_code=201)
def sign_up(formData: User):
    try:
        dynamoDB_handler.post_user_table(formData)
        return {"message": "User created successfully!"}
    except:
        raise HTTPException(status_code=401)

@router.post("/login", status_code=200)
def sign_in(formData: SignIn, response:Response):
    user_info = formData.__dict__
    db_response = dynamoDB_handler.get_user_info(user_info['email'])
    try:
        pass_verification = dynamoDB_handler.verify_password(user_info['password'],db_response['Items'][0]['password'])
        if pass_verification:
            del db_response['Items'][0]['password']
            return {"message":"Correct credentials","user_info":db_response['Items']}
        else:
            response.status_code=401
            return {"message":"Wrong Credentials"}
    except Exception as e:
        print(e)
        response.status_code = 500
        return {"message": "Wrong Credentials"}
