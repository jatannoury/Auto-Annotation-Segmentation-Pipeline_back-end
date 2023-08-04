from routes import users
from routes import projects
from routes.ml_models import instant_prediction
routers = {
    'users': users.router,
    'project': projects.router,
    "instant_prediction":instant_prediction.router
}
