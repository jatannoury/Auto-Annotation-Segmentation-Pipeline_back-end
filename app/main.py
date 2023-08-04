import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import routers

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this to the appropriate list of allowed origins
    allow_methods=["*"],  # Set this to the appropriate list of allowed HTTP methods
    allow_headers=["*"],  # Set this to the appropriate list of allowed headers
)


app.include_router(routers['users'], prefix='/users')
app.include_router(routers['project'], prefix='/project')
app.include_router(routers['instant_prediction'], prefix='/ml_models/instant_prediction')
@app.get("/")
def ping():
    return {"message": "Ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
