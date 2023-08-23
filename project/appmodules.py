from injector import inject

from src.repository.sql_alchemy_repository import Repository
from src.repository.sql_alchemy_repository import SqlAlchemyRepository
from src.media.aws_service import MediaService
from src.media.aws_service import AwsService
from src.service.share_service import ShareService

aws_service = AwsService(
    'https://sqs.us-east-1.amazonaws.com/869305664526/shared-spaces.fifo')

sql_alchemy_repository = SqlAlchemyRepository()


def repository(binder):
    binder.bind(
        Repository,
        to=sql_alchemy_repository
    )


def media_service(binder):
    binder.bind(
        MediaService,
        to=aws_service
    )


def share_service(binder):
    binder.bind(
        ShareService,
        to=ShareService(sql_alchemy_repository, aws_service)
    )
