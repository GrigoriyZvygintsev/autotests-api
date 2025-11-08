from typing import TypedDict
from httpx import Response
from clients.api_client import APIClient
from clients.private_http_builder import AuthenticationUserDict, get_private_http_client


class GetExercisesQueryDict(TypedDict):
    """Параметры запроса для получения списка упражнений."""
    courseId: str


class CreateExerciseRequest(TypedDict):
    """Данные для создания нового упражнения."""
    title: str
    courseId: str
    maxScore: int | None
    minScore: int | None
    orderIndex: int
    description: str
    estimatedTime: str | None


class UpdateExerciseRequest(TypedDict):
    """Данные для частичного обновления упражнения. Поля опциональны."""
    title: str | None
    maxScore: int | None
    minScore: int | None
    orderIndex: int | None
    description: str | None
    estimatedTime: str | None

class Exercise(TypedDict):
    """Модель данных для одного упражнения."""
    id: str
    title: str
    courseId: str
    maxScore: int | None
    minScore: int | None
    orderIndex: int
    description: str
    estimatedTime: str | None

class GetExercisesResponseDict(TypedDict):
    """Модель ответа для списка упражнений."""
    Items: list[Exercise]

class GetExerciseResponseDict(TypedDict):
    """Модель ответа для одного упражнения."""
    exercises: Exercise

class ExercisesClient(APIClient):
    """
    Клиент для работы с упражнениями (exercises) через API.

    Предоставляет методы для получения, создания, обновления и удаления упражнений.
    """

    def get_exercises_api(self, query: GetExercisesQueryDict) -> Response:
        """
        Получает список упражнений по заданному courseId.

        :param query: Параметры фильтрации (обязательно courseId).
        :type query: GetExercisesQueryDict
        :return: HTTP-ответ со списком упражнений.
        :rtype: httpx.Response
        """
        return self.get("/api/v1/exercises", params=query)

    def get_exercise_api(self, exercise_id: str) -> Response:
        """
        Получает упражнение по его идентификатору.

        :param exercise_id: Уникальный идентификатор упражнения.
        :type exercise_id: str
        :return: HTTP-ответ с данными упражнения.
        :rtype: httpx.Response
        """
        return self.get(f"/api/v1/exercises/{exercise_id}")

    def create_exercise_api(self, request: CreateExerciseRequest) -> Response:
        """
        Создаёт новое упражнение.

        :param request: Данные для создания упражнения.
        :type request: CreateExerciseRequest
        :return: HTTP-ответ с данными созданного упражнения.
        :rtype: httpx.Response
        """
        return self.post("/api/v1/exercises", json=request)

    def update_exercise_api(self, exercise_id: str, request: UpdateExerciseRequest) -> Response:
        """
        Частично обновляет упражнение по его идентификатору.

        :param exercise_id: Уникальный идентификатор упражнения.
        :type exercise_id: str
        :param request: Поля для обновления (может содержать только те, что нужно изменить).
        :type request: UpdateExerciseRequest
        :return: HTTP-ответ с обновлёнными данными упражнения.
        :rtype: httpx.Response
        """
        return self.patch(f"/api/v1/exercises/{exercise_id}", json=request)

    def delete_exercise_api(self, exercise_id: str) -> Response:
        """
        Удаляет упражнение по его идентификатору.

        :param exercise_id: Уникальный идентификатор упражнения.
        :type exercise_id: str
        :return: HTTP-ответ с подтверждением удаления (обычно 204 No Content).
        :rtype: httpx.Response
        """
        return self.delete(f"/api/v1/exercises/{exercise_id}")

    def get_exercise(self, exercise_id: str) -> GetExerciseResponseDict:
        """
        Получает одно упражнение по ID и возвращает его в виде словаря.

        :param exercise_id: Уникальный идентификатор упражнения.
        :return: Данные упражнения.
        """
        response = self.get_exercise_api(exercise_id)
        return response.json()

    def get_exercises(self, query: GetExercisesQueryDict) -> GetExercisesResponseDict:
        """
        Получает список упражнений по фильтру и возвращает его в виде словаря.

        :param query: Параметры фильтрации (например, courseId).
        :return: Список упражнений.
        """
        response = self.get_exercises_api(query)
        return response.json()

    def create_exercise(self, request: CreateExerciseRequest) -> GetExerciseResponseDict:
        """
        Создаёт новое упражнение и возвращает созданный объект.

        :param request: Данные для создания упражнения.
        :return: Данные созданного упражнения.
        """
        response = self.create_exercise_api(request)
        return response.json()

    def update_exercise(self, exercise_id: str, request: UpdateExerciseRequest) -> GetExerciseResponseDict:
        """
        Обновляет существующее упражнение и возвращает обновлённый объект.

        :param exercise_id: ID упражнения для обновления.
        :param request: Поля и значения для обновления.
        :return: Обновлённые данные упражнения.
        """
        response = self.update_exercise_api(exercise_id, request)
        return response.json()

def get_exercises_client(user: AuthenticationUserDict) -> ExercisesClient:
    """Фабричная функция для создания экземпляра ExercisesClient с аутентификацией."""
    return ExercisesClient(client=get_private_http_client(user))