from flask import request

from src.repository.sql_alchemy_repository import SqlAlchemyRepository


def repository(binder):
    binder.bind(
        SqlAlchemyRepository,
        to=SqlAlchemyRepository,
        scope=request
    )
