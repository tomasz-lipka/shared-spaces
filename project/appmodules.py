from injector import Module

from src.repository.sql_alchemy_repository import Repository
from src.repository.sql_alchemy_repository import SqlAlchemyRepository
from src.media.aws_service import MediaService
from src.media.aws_service import AwsService
from src.service.share_service import ShareService
from src.service.assignment_service import AssignmentService
from src.service.validator_helper import ValidatorHelper


class AppModules(Module):

    SQS_URL = 'https://sqs.us-east-1.amazonaws.com/869305664526/shared-spaces.fifo'

    def __init__(self, repo_url):
        self.repo_url = repo_url
        self.sql_alchemy_repository = SqlAlchemyRepository(repo_url)
        self.validator = ValidatorHelper(self.sql_alchemy_repository)
        self.aws_service = AwsService(
            self.SQS_URL,
            self.validator
        )

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
            to=ShareService(self.sql_alchemy_repository,
                            self.aws_service,
                            self.validator
                            )
        )
        binder.bind(
            AssignmentService,
            to=AssignmentService(self.sql_alchemy_repository,
                                 self.validator
                                 )
        )
        binder.bind(
            ValidatorHelper,
            to=self.validator
        )
