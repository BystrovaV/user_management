from abc import ABC, abstractmethod
from typing import BinaryIO


class ImageRepository(ABC):
    @abstractmethod
    async def upload_image(self, file: BinaryIO, filename: str) -> str:
        pass
