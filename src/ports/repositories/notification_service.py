from abc import ABC, abstractmethod


class NotificationService(ABC):
    @abstractmethod
    def publish_message(self, email: str, msg: str, subject: str):
        pass
