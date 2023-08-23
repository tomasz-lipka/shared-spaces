from flask import request

from src.repository.sql_alchemy_repository import Repository
from src.repository.sql_alchemy_repository import SqlAlchemyRepository
from src.media.aws_service import MediaService
from src.media.aws_service import AwsService


def repository(binder):
    binder.bind(
        Repository,
        to=SqlAlchemyRepository()
    )


def media_service(binder):
    binder.bind(
        MediaService,
        to=AwsService('https://sqs.us-east-1.amazonaws.com/869305664526/shared-spaces.fifo')
    )
