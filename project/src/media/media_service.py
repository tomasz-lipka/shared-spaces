from abc import ABC, abstractmethod
from flask_login import login_required


class MediaService(ABC):

    @abstractmethod
    @login_required
    def upload_image(self, file, space_id, share_id):
        """
        """

    @abstractmethod
    @login_required
    def get_image(self, share):
        """
        """

    @abstractmethod
    @login_required
    def delete_space_directory(self, space):
        """
        """

    @abstractmethod
    @login_required
    def get_all_media_urls(self, space_id):
        """
        """

    @abstractmethod
    def create_temp_directory(self):
        """
        """
