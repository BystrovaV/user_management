import pytest

from core.exceptions import TokenDenied


@pytest.mark.asyncio
async def test_signup_use_case(signup_use_case, user_repository, user_test):
    user_id = await signup_use_case(user=user_test)

    assert user_id is not None
    assert await user_repository.get_user(user_id) is not None


@pytest.mark.asyncio
async def test_login_use_case(
    signup_use_case, login_use_case, user_repository, user_test
):
    user_id = await signup_use_case(user=user_test)

    assert await user_repository.get_user(user_id) is not None

    token = await login_use_case(
        {"user_data": user_test.username, "password": "1234567"}
    )
    assert token is not None


@pytest.mark.asyncio
async def test_get_current_user_use_case(
    get_current_user_use_case,
    user_test,
    user_repository,
    signup_use_case,
    login_use_case,
):
    user_id = await signup_use_case(user=user_test)

    assert await user_repository.get_user(user_id) is not None

    token = (
        await login_use_case({"user_data": user_test.username, "password": "1234567"})
    ).get("access_token")
    print("Token: ", token)

    user = await get_current_user_use_case(token)
    assert user == user_test


@pytest.mark.asyncio
async def test_get_current_user_in_blacklist(
    get_current_user_use_case,
    user_test,
    user_repository,
    signup_use_case,
    login_use_case,
    blacklist_repository,
):
    user_id = await signup_use_case(user=user_test)

    assert await user_repository.get_user(user_id) is not None

    token = (
        await login_use_case({"user_data": user_test.username, "password": "1234567"})
    ).get("access_token")
    blacklist_repository.blacklist[token] = token

    with pytest.raises(TokenDenied):
        await get_current_user_use_case(token)


@pytest.mark.asyncio
async def test_refresh_token_use_case(
    signup_use_case,
    user_test,
    user_repository,
    login_use_case,
    refresh_token_use_case,
    blacklist_repository,
):
    await signup_use_case(user=user_test)

    old_token = (
        await login_use_case({"user_data": user_test.username, "password": "1234567"})
    ).get("access_token")
    token = (await refresh_token_use_case(old_token)).get("access_token")

    assert token is not None
    assert token != old_token

    assert await blacklist_repository.check(old_token)
