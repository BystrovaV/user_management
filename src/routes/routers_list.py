from app import app
from routes import auth, group, healthcheck, user, users

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(group.router)
app.include_router(healthcheck.router)
