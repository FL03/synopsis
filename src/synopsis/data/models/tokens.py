from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator

from synopsis.data.primitives import ModelController as Mc


class Tokens(Model):
    access_type = fields.CharField(Mc.strings.sm)
    token = fields.CharField(Mc.strings.lg)


Token = pydantic_model_creator(Tokens, name="Token")
TokenIn = pydantic_model_creator(Tokens, name="TokenIn", exclude_readonly=True)
