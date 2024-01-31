from abc import ABC, abstractmethod

from domain.group import Group


class GroupRepository(ABC):
    @abstractmethod
    async def get_groups(self) -> list[Group]:
        pass
