"""
Module for Application dependency injection management.
"""
from injector import Module

from src.repository.sql_alchemy_repository import Repository
from src.repository.sql_alchemy_repository import SqlAlchemyRepository
from src.media.image_service import ImageService
from src.media.aws_image_service import AwsImageService
from src.service.share_service import ShareService
from src.service.assignment_service import AssignmentService
from src.service.validator_helper import ValidatorHelper


class AppModules(Module):
    """
    This class defines dependencies within the application. 
    It sets up bindings for various services and repositories used throughout the application.
    """

    def __init__(self, app):
        self.sql_alchemy_repository = SqlAlchemyRepository(
            app.config['DATABASE_URL'])
        self.validator = ValidatorHelper(self.sql_alchemy_repository)
        self.aws_image_service = AwsImageService(
            app.config['SQS_URL'],
            app.config['S3_TEMP_BUCKET'],
            app.config['MODE'],
            self.validator
        )

    def configure(self, binder):
        binder.bind(
            Repository,
            to=self.sql_alchemy_repository
        )
        binder.bind(
            ImageService,
            to=self.aws_image_service
        )
        binder.bind(
            ShareService,
            to=ShareService(self.sql_alchemy_repository,
                            self.aws_image_service,
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
