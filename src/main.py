import logging
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app import service
from app.models import get_session
from app.schemas import UserBase, UsersQueryParams
from app.settings import Settings
from routers import auth, group, user

app = FastAPI()
app.include_router(user.router)
app.include_router(group.router)
app.include_router(auth.router)

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

SessionDependency = Annotated[AsyncSession, Depends(get_session)]


# -------------------
@app.get("/")
def read_root():
    html_content = "<h2>Hello World!</h2>"

    # validate user
    try:
        # name="", surname="", username="", email="test1@test.com"
        user = UserBase(phone_number="+375 44 562-24")
        logger.info(user)
    except ValidationError as e:
        logger.info(e)

    # test settings
    cnf = Settings()
    logger.info(cnf.get_db_url)

    return HTMLResponse(content=html_content)


@app.get("/users")
async def get_users(
    session: SessionDependency, params: Annotated[UsersQueryParams, Depends()]
):
    users = await service.get_users(session, params)

    return [
        UserBase(
            name=x.name,
            surname=x.surname,
            username=x.username,
            phone_number=x.phone_number,
            email=x.email,
        )
        for x in users
    ]


# ----------------
@app.post("/users")
async def add_user(user: UserBase, session: SessionDependency):
    user = service.insert_user(session, user)

    try:
        await session.commit()
        logger.info(user)
        return user
    except IntegrityError as ex:
        await session.rollback()
        logger.error("The user is already stored")
        return "The user is already stored"
