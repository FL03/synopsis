import random
from synopsis.utils.generators import create_random_string, rand_float, rand_option
from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator


class Items(Model):
    id = fields.IntField(pk=True)
    created = fields.DatetimeField(auto_now_add=True)
    modified = fields.DatetimeField(auto_now=True)

    item = fields.CharField(120, null=False)
    classification = fields.CharField(120, null=False)
    count = fields.IntField(False, default=0)
    description = fields.CharField(120, null=False)


Item = pydantic_model_creator(Items, name="Item")
ItemIn = pydantic_model_creator(Items, exclude_readonly=True, name="ItemIn")


def generate_entries(m: int = 100):
    classifications = ["meat", "chicken", "veal", "turkey"]
    data = [
        ItemIn(
            item=create_random_string(random.randint(8, 16)),
            classification=rand_option(*classifications),
            description=create_random_string(random.randint(20, 30)),
            count=random.randint(0, 100)
        )
        for i in range(1, m+1)
    ]
    return data[:]


if __name__ == "__main__":
    print(generate_entries())
