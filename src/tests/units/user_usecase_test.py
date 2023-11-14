import pytest

from adapters.repositories.in_memory_user_repository import InMemoryUserRepository
from domain.group import Group
from domain.user import RoleEnum, User
from usecase.user_usecase import GetUsersUseCase

# @pytest.fixture
# def user_repository():
#     return InMemoryUserRepository()
#
#
# @pytest.fixture
# def save_user_use_case(user_repository):
#     return SaveUserUseCase(user_repository)
#
#
# @pytest.fixture
# def get_users_use_case(user_repository):
#     return GetUsersUseCase(user_repository)
#
#
# @pytest.mark.asyncio
# async def test_save_user(
#         save_user_use_case: SaveUserUseCase,
#         user_repository: InMemoryUserRepository
#         ):
#     user = await save_user_use_case(user=User(
#         name="test1", surname="test1", username="test1",
#         phone_number="+375 44 562-24-75", email="test1@gtest1.com", group=Group(id=1),
#         role=RoleEnum.user
#     ))
#
#     assert user_repository.users[0] is not None
#
#
# @pytest.mark.asyncio
# async def test_get_users(
#         get_users_use_case: GetUsersUseCase,
#         save_user_use_case: SaveUserUseCase,
#         user_repository: InMemoryUserRepository
#     ):
#     user1 = await save_user_use_case(user=User(
#         name="test1", surname="test1", username="test1",
#         phone_number="+375 44 111-11-11", email="test1@gtest1.com", group=Group(id=1),
#         role=RoleEnum.user
#     ))
#
#     user2 = await save_user_use_case(user=User(
#         name="test2", surname="test2", username="test2",
#         phone_number="+375 44 222-22-22", email="test2@gtest2.com", group=Group(id=1),
#         role=RoleEnum.user
#     ))
#
#     user3 = await save_user_use_case(user=User(
#         name="test3", surname="test3", username="test3",
#         phone_number="+375 44 333-33-33", email="test3@gtest3.com", group=Group(id=3),
#         role=RoleEnum.user
#     ))
#
#     assert len(await get_users_use_case()) == 3
