from typing import TypedDict
from httpx import Response
from clients.api_client import APIClient

class CreateUserRequest(TypedDict):
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
    def create_user_api(self, request: CreateUserRequest) -> Response:
        """
        Выполняет POST-запрос для создания нового пользователя.

        :param request: Словарь с данными пользователя, соответствующий структуре CreateUserRequest.
                        Должен содержать:
                        - email: уникальный email пользователя
                        - password: пароль
                        - lastName: фамилия
                        - firstName: имя
                        - middleName: отчество
        :type request: CreateUserRequest
        :return: Объект Response с результатом HTTP-запроса.
                 При успехе возвращает 201 Created и данные пользователя.
        :rtype: httpx.Response
        """
        return self.client.post('/api/v1/users', json=request)