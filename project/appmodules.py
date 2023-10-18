"""
Module for Application dependency injection management.
"""
from injector import Module

from src.repository.sql_alchemy_repository import Repository
from src.repository.sql_alchemy_repository import SqlAlchemyRepository
from src.service.image.image_service import ImageService
from src.service.image.aws_image_service import AwsImageService
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
        self.aws_image_service = AwsImageService(app, self.validator)

    def configure(self, binder):
        binder.bind(
            Repository,
            to=self.sql_alchemy_repository
        )
        binder.bind(
            ImageService,
            to=self.aws_image_service
        )
