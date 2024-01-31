import logging.config

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routes.add_exception_hadlers import add_exception_handlers

app = FastAPI()
add_exception_handlers(app)

origins = ["http://localhost:3000", "localhost:3000"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
