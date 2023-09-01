"""
Module for Application dependency injection management.
"""
from injector import Module

from src.repository.sql_alchemy_repository import Repository
from src.repository.sql_alchemy_repository import SqlAlchemyRepository
from src.service.image.image_service import ImageService
from src.service.image.aws_image_service import AwsImageService
from src.service.entity.share_service import ShareService
from src.service.entity.assignment_service import AssignmentService
from src.service.helper.service_validator import ServiceValidator


class AppModules(Module):
    """
    This class defines dependencies within the application. 
    It sets up bindings for various services and repositories used throughout the application.
    """

    def __init__(self, app):
        self.sql_alchemy_repository = SqlAlchemyRepository(
            app.config['DATABASE_URL'])
        self.validator = ServiceValidator(self.sql_alchemy_repository)
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
            ServiceValidator,
            to=self.validator
        )
