from tortoise.contrib.fastapi import register_tortoise


def dbc(app, models: list, uri: str = "sqlite://./local.db", **kwargs):
    default_kwargs: dict = dict(add_exception_handlers=True, generate_schemas=True)
    register_tortoise(
        app,
        db_url=uri,
        modules=dict(models=models[:]),
        **dict(default_kwargs, **kwargs)
    )
