from typing import TypedDict
from httpx import Response
from clients.api_client import APIClient


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