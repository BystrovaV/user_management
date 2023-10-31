import logging
import sys

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.models import engine
from app.settings import Settings

app = FastAPI()

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


@app.get("/")
def read_root():
    html_content = "<h2>Hello World!</h2>"

    cnf = Settings()
    logger.info(cnf.get_db_url)
    return HTMLResponse(content=html_content)
