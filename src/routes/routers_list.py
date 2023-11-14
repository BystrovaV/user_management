from app import app
from routes import auth, user

app.include_router(user.router)
# app.include_router(group.router)
app.include_router(auth.router)
