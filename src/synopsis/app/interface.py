import datetime
import dotenv
from fastapi import FastAPI, responses
from pydantic import BaseModel
from tortoise.contrib.fastapi import register_tortoise

from synopsis.core.session import Session
from synopsis.app.api import index

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


register_tortoise(
    app,
    add_exception_handlers=True,
    db_url=session.settings.db_uri,
    generate_schemas=True,
    modules=dict(models=["synopsis.data.models"])
)


def run():
    import uvicorn
    uvicorn.run(
        "synopsis.app.interface:app",
        host="0.0.0.0",
        port=session.settings.server_port,
        reload=session.settings.dev_mode
    )
