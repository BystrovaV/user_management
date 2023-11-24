import logging.config

from fastapi import FastAPI

from routes.add_exception_hadlers import add_exception_handlers

app = FastAPI()
add_exception_handlers(app)

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
