from abc import ABC, abstractmethod


class MediaService(ABC):

    @abstractmethod
    def upload_image(self, file, share_id):
        """
        """

    @abstractmethod
    def get_image(self, share):
        """
        """

    @abstractmethod
    def delete_space_directory(self, space):
        """
        """

    @abstractmethod
    def get_all_media_urls(self, space_id):
        """
        """

    @abstractmethod
    def create_temp_directory(self):
        """
        """
