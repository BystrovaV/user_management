import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from dependencies.dependencies import (
    delete_user_use_case,
    get_current_user,
    get_login_use_case,
    get_refresh_token_use_case,
    get_reset_password_use_case,
    get_signup_use_case,
    get_user_use_case,
    get_users_use_case,
    update_user_use_case,
)
from main import app as main_app
from tests.units.endpoints_tests.mocks import (
    mock_delete_user,
    mock_get_current_user,
    mock_get_user,
    mock_get_users,
    mock_login,
    mock_refresh,
    mock_reset,
    mock_signup,
    mock_update_user,
)


@pytest.fixture(scope="module")
def app():
    main_app.dependency_overrides[get_signup_use_case] = mock_signup
    main_app.dependency_overrides[get_login_use_case] = mock_login
    main_app.dependency_overrides[get_refresh_token_use_case] = mock_refresh
    main_app.dependency_overrides[get_reset_password_use_case] = mock_reset
    main_app.dependency_overrides[get_current_user] = mock_get_current_user
    main_app.dependency_overrides[update_user_use_case] = mock_update_user
    main_app.dependency_overrides[delete_user_use_case] = mock_delete_user
    main_app.dependency_overrides[get_user_use_case] = mock_get_user
    main_app.dependency_overrides[get_users_use_case] = mock_get_users

    _app = main_app
    yield _app


@pytest.fixture(scope="module")
def client(app: FastAPI):
    with TestClient(app) as client:
        yield client
