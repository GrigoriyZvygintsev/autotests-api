from typing import TypedDict
from httpx import Response
from clients.api_client import APIClient
from clients.public_http_builder import get_public_http_client

class User(TypedDict):
    id: str
    email: str
    lastName: str
    firstName: str
    middleName: str

class CreateUserResponseDict(TypedDict):
    user: User

class CreateUserRequestDict(TypedDict):
    """Типизированный словарь для данных создания пользователя."""
    email: str
    password: str
    lastName: str
    firstName: str
    middleName: str


class PublicUsersClient(APIClient):
    """
    Клиент для работы с публичными методами эндпоинта /api/v1/users.

    Предназначен для операций, не требующих авторизации, например, создания пользователя.
    """
    def create_user_api(self, request: CreateUserRequestDict) -> Response:
        """
        Выполняет POST-запрос для создания нового пользователя.

        :param request: Словарь с данными пользователя, соответствующий структуре CreateUserRequest.
                        Должен содержать:
                        - email: уникальный email пользователя
                        - password: пароль
                        - lastName: фамилия
                        - firstName: имя
                        - middleName: отчество
        :type request: CreateUserRequestDict
        :return: Объект Response с результатом HTTP-запроса.
                 При успехе возвращает 201 Created и данные пользователя.
        :rtype: httpx.Response
        """
        return self.client.post('/api/v1/users', json=request)

    def create_user(self, request: CreateUserRequestDict) -> CreateUserResponseDict:
        response = self.create_user_api(request)
        return response.json()



def get_public_users_client() -> PublicUsersClient:
    return PublicUsersClient(client=get_public_http_client())