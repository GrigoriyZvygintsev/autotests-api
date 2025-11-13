from http import HTTPStatus

from clients.authentication.authentication_client import get_authentication_client
from clients.authentication.authentication_schema import LoginRequestSchema, LoginResponseSchema
from clients.users.public_users_client import get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema
from tools.assertions.authentication import assert_login_response
from tools.assertions.base import assert_status_code, assert_is_true
from tools.assertions.schema import validate_json_schema


def test_login():
    public_users_client = get_public_users_client()
    request_create_user = CreateUserRequestSchema()
    response_create_user = public_users_client.create_user(request_create_user)

    authentication_client = get_authentication_client()
    request_authentication_user = LoginRequestSchema(email=request_create_user.email, password=request_create_user.password)
    response_authentication_user = authentication_client.login_api(request_authentication_user)
    response_authentication_user_data =  LoginResponseSchema.model_validate_json(response_authentication_user.text)
    print(response_authentication_user_data)

    assert_status_code(response_authentication_user.status_code, HTTPStatus.OK)
    assert_login_response(response_authentication_user_data)

    validate_json_schema(response_authentication_user.json(), response_authentication_user_data.model_json_schema())

