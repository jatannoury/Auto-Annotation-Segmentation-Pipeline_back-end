from routes import users
from routes import projects

routers = {
    'users': users.router,
    'project': projects.router,
}
