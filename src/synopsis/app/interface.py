import datetime

from fastapi import FastAPI, responses
from pydantic import BaseModel

from synopsis.app.api import index
from synopsis.core.session import Session
from synopsis.data.database import dbc

app = FastAPI()
session: Session = Session()


class AppEventMessage(BaseModel):
    context: str
    message: str
    timestamp: str = str(datetime.datetime.now())


@app.on_event("startup")
async def startup():
    print(
        AppEventMessage(
            context="startup",
            message="View the application locally at http://localhost:{}".format(session.settings.server_port)
        )
    )


@app.get("/")
async def root() -> responses.RedirectResponse:
    return responses.RedirectResponse("/docs")


@app.on_event("shutdown")
async def shutdown():
    print(AppEventMessage(context="shutdown", message="Terminating the application..."))


app.include_router(router=index.router)

db_models = [
    "synopsis.data.models.items",
    "synopsis.data.models.tokens",
    "synopsis.data.models.users"
]

dbc(app, db_models, session.settings.db_uri)


def run():
    import uvicorn
    uvicorn.run(
        "synopsis.app.interface:app",
        host="0.0.0.0",
        port=session.settings.server_port,
        reload=session.settings.dev_mode
    )
