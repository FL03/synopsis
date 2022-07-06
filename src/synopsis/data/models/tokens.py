from pydantic import BaseModel
from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator

from synopsis.data.primitives import ModelController as Mc


class Tokens(Model):
    access_token = fields.CharField(Mc.strings.lg)
    token_type = fields.CharField(Mc.strings.lg)

    class PydanticMeta:
        exclude = ["id"]


class TokenData(BaseModel):
    username: str


Token = pydantic_model_creator(Tokens, name="Token")
TokenIn = pydantic_model_creator(Tokens, name="TokenIn", exclude_readonly=True)
