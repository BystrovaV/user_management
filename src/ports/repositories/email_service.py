from abc import ABC, abstractmethod


class EmailService(ABC):
    @abstractmethod
    async def send_email(self, email: str, text: str):
        pass
