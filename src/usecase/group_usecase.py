from domain.group import Group
from ports.repositories.group_repository import GroupRepository


class GetGroupsUseCase:
    def __init__(self, group_repository: GroupRepository):
        self.group_repository = group_repository

    async def __call__(self) -> list[Group]:
        return await self.group_repository.get_groups()
