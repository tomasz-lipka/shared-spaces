from injector import Module

from src.repository.sql_alchemy_repository import Repository
from src.repository.sql_alchemy_repository import SqlAlchemyRepository
from src.media.aws_service import MediaService
from src.media.aws_service import AwsService
from src.service.share_service import ShareService


class AppModules(Module):

    aws_service = AwsService(
        'https://sqs.us-east-1.amazonaws.com/869305664526/shared-spaces.fifo')
    sql_alchemy_repository = SqlAlchemyRepository()

    def configure(self, binder):
        binder.bind(
            Repository,
            to=self.sql_alchemy_repository
        )
        binder.bind(
            MediaService,
            to=self.aws_service
        )
        binder.bind(
            ShareService,
            to=ShareService(self.sql_alchemy_repository, self.aws_service)
        )
