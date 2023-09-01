"""
Module containing an ImageService ABC (Abstract Base Class).
"""
from abc import ABC, abstractmethod


class MediaService(ABC):
    """
    Abstract base class for managing image files associated with shares.
    """

    @abstractmethod
    def upload_image(self, file, share_id):
        """
        Upload an image related to a share.
        Args:
            file (file object): The image file to be uploaded.
            share_id (int): ID of the share to which the image corresponds.
        """

    @abstractmethod
    def get_image(self, share):
        """
        Retrieve the image related to a specific share.
        Args:
            share (Share): The Share object for which to retrieve the image.
        Returns:
            image item.
        """

    @abstractmethod
    def delete_space_directory(self, space):
        """
        Delete the directory associated with a space, including all its contents.
        Args:
            space (Space): The Space object for which to delete the directory.
        """

    @abstractmethod
    def get_all_media_urls(self, space_id):
        """
        Retrieve a list of all images associated with a specific space.
        Args:
            space_id (int): ID of the target space.
        Returns:
            list: A list of image items.
        """

    @abstractmethod
    def create_temp_directory(self):
        """
        Create a temporary directory for file upload.
        """
