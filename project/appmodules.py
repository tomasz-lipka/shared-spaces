from injector import Module

from src.repository.sql_alchemy_repository import Repository
from src.repository.sql_alchemy_repository import SqlAlchemyRepository
from src.media.aws_service import MediaService
from src.media.aws_service import AwsService
from src.service.share_service import ShareService
from src.service.assignment_service import AssignmentService
from src.service.validator_helper import ValidatorHelper


class AppModules(Module):

    sql_alchemy_repository = SqlAlchemyRepository()
    validator = ValidatorHelper(sql_alchemy_repository)
    aws_service = AwsService(
        'https://sqs.us-east-1.amazonaws.com/869305664526/shared-spaces.fifo',
        validator
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
