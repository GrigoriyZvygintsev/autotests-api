import pytest
from http import HTTPStatus

from _pytest.fixtures import SubRequest

from clients.users.public_users_client import get_public_users_client, PublicUsersClient
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.users import assert_create_user_response
from tools.fakers import fake


@pytest.mark.users
@pytest.mark.regression
@pytest.mark.parametrize('domain', ['mail.ru', 'gmail.com', 'example.com'])
def test_create_user(domain: str, public_users_client: PublicUsersClient):
    request = CreateUserRequestSchema(email=fake.email(domain=domain))
    response = public_users_client.create_user_api(request)
    # Инициализируем модель ответа на основе полученного JSON в ответе
    # Также благодаря встроенной валидации в Pydantic дополнительно убеждаемся, что ответ корректный
    response_data = CreateUserResponseSchema.model_validate_json(response.text)

    assert_status_code(response.status_code, HTTPStatus.OK)
    # Используем функцию для проверки ответа создания юзера
    assert_create_user_response(request, response_data)

    validate_json_schema(response.json(), response_data.model_json_schema())


@pytest.fixture(params=['url1', 'url2', 'url3'])
def host(request: SubRequest):
    return request.param


def test_host(host: str):
    # Используем фикстуру в автотесте, она вернет нам хост в виде строки
    print(f"Running test on host: {host}")