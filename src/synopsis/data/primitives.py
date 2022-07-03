from pydantic import BaseModel


class Sized(BaseModel):
    sm: int
    md: int
    lg: int


class ModelController(object):
    strings: Sized = Sized(sm=64, md=128, lg=256)


class Status(BaseModel):
    message: str

