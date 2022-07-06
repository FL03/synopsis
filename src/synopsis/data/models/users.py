"""
    Appellation: Users
    Context: module
    Creator: FL03 <jo3mccain@icloud.com>
    Description:
        Describe the standard models surrounding users and their data
"""

from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator

from synopsis.data.primitives import ModelController as Mc


class Accounts(Model):
    id = fields.IntField(pk=True)
    user: fields.ForeignKeyRelation["Users"] = fields.ForeignKeyField("models.Users", related_name="account")
    ensname = fields.CharField(Mc.strings.md)
    primary_email = fields.CharField(Mc.strings.md)

    category = fields.CharField(Mc.strings.sm, default="user")
    classification = fields.CharField(Mc.strings.sm, default="active")

    address: fields.ReverseRelation["Addresses"]
    slip: fields.ReverseRelation["Slips"]

    class PydanticMeta:
        computed = []
        exclude = []


class Addresses(Model):
    id = fields.IntField(pk=True)
    account: fields.ForeignKeyRelation["Accounts"] = fields.ForeignKeyField("models.Accounts", related_name="address")

    street = fields.CharField(Mc.strings.md, null=True)
    suffix = fields.CharField(Mc.strings.sm, null=True)
    zip_code = fields.CharField(Mc.strings.sm, null=True)

    created = fields.DatetimeField(auto_now_add=True)
    modified = fields.DatetimeField(auto_now=True)

    class PydanticMeta:
        computed = []
        exclude = []


class Slips(Model):
    id = fields.IntField(pk=True)
    account: fields.ForeignKeyRelation["Accounts"] = fields.ForeignKeyField("models.Accounts", related_name="slip")
    created = fields.DatetimeField(auto_now_add=True)
    classification = fields.CharField(Mc.strings.sm, default="server", null=False)
    duration = fields.FloatField(default=0.0, null=False)
    context = fields.CharField(Mc.strings.sm, default="MID", null=False)
    sales = fields.FloatField(default=0.0, null=False)
    drawer = fields.FloatField(default=0.0, null=False)
    amount = fields.FloatField(default=0.0)

    class PydanticMeta:
        computed = []
        exclude = []


class Users(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(Mc.strings.sm, unique=True)
    password_hash = fields.CharField(Mc.strings.md, null=True)
    disabled = fields.BooleanField(default=False, null=True)

    created = fields.DatetimeField(auto_now_add=True)
    modified = fields.DatetimeField(auto_now=True)

    account: fields.ReverseRelation["Accounts"]

    class PydanticMeta:
        computed = []
        exclude = ["password_hash"]


'''
    Leverage tortoise-orm to convert the models into pydantic data-structures for minimal code
'''
Account = pydantic_model_creator(Accounts, name="Profile")
AccountIn = pydantic_model_creator(Accounts, name="ProfileIn", exclude_readonly=True)

Address = pydantic_model_creator(Addresses, name="Address")
AddressIn = pydantic_model_creator(Addresses, name="AddressIn", exclude_readonly=True)

Slip = pydantic_model_creator(Slips, name="Slip")
SlipIn = pydantic_model_creator(Slips, exclude_readonly=True, name="SlipIn")

User = pydantic_model_creator(Users, name="User")
UserIn = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True)
