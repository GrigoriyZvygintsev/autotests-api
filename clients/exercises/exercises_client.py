from httpx import Response
from clients.api_client import APIClient
from clients.private_http_builder import get_private_http_client, AuthenticationUserSchema
from clients.exercises.exercises_schema import (
    GetExercisesQuerySchema,
    CreateExerciseRequestSchema,
    UpdateExerciseRequestSchema,
    GetExercisesResponseSchema,
    GetExerciseResponseSchema,
)

class ExercisesClient(APIClient):
    """
    Клиент для работы с упражнениями (exercises) через API.

    Предоставляет методы для получения, создания, обновления и удаления упражнений.
    """

    def get_exercises_api(self, query: GetExercisesQuerySchema) -> Response:
        """
        Получает список упражнений по заданному courseId.

        :param query: Параметры фильтрации (обязательно courseId).
        :type query: GetExercisesQuerySchema
        :return: HTTP-ответ со списком упражнений.
        :rtype: httpx.Response
        """
        return self.get("/api/v1/exercises", params=query.model_dump(by_alias=True, exclude_none=True))

    def get_exercise_api(self, exercise_id: str) -> Response:
        """
        Получает упражнение по его идентификатору.

        :param exercise_id: Уникальный идентификатор упражнения.
        :type exercise_id: str
        :return: HTTP-ответ с данными упражнения.
        :rtype: httpx.Response
        """
        return self.get(f"/api/v1/exercises/{exercise_id}")

    def create_exercise_api(self, request: CreateExerciseRequestSchema) -> Response:
        """
        Создаёт новое упражнение.

        :param request: Данные для создания упражнения.
        :type request: CreateExerciseRequestSchema
        :return: HTTP-ответ с данными созданного упражнения.
        :rtype: httpx.Response
        """
        return self.post("/api/v1/exercises", json=request.model_dump(by_alias=True))

    def update_exercise_api(self, exercise_id: str, request: UpdateExerciseRequestSchema) -> Response:
        """
        Частично обновляет упражнение по его идентификатору.

        :param exercise_id: Уникальный идентификатор упражнения.
        :type exercise_id: str
        :param request: Поля для обновления (может содержать только те, что нужно изменить).
        :type request: UpdateExerciseRequestSchema
        :return: HTTP-ответ с обновлёнными данными упражнения.
        :rtype: httpx.Response
        """
        return self.patch(
            f"/api/v1/exercises/{exercise_id}",
            json=request.model_dump(by_alias=True, exclude_none=True),
        )

    def delete_exercise_api(self, exercise_id: str) -> Response:
        """
        Удаляет упражнение по его идентификатору.

        :param exercise_id: Уникальный идентификатор упражнения.
        :type exercise_id: str
        :return: HTTP-ответ с подтверждением удаления (обычно 204 No Content).
        :rtype: httpx.Response
        """
        return self.delete(f"/api/v1/exercises/{exercise_id}")

    def get_exercise(self, exercise_id: str) -> GetExerciseResponseSchema:
        """
        Получает одно упражнение по ID и возвращает его в виде словаря.

        :param exercise_id: Уникальный идентификатор упражнения.
        :return: Данные упражнения.
        """
        response = self.get_exercise_api(exercise_id)
        return GetExerciseResponseSchema.model_validate_json(response.text)

    def get_exercises(self, query: GetExercisesQuerySchema) -> GetExercisesResponseSchema:
        """
        Получает список упражнений по фильтру и возвращает его в виде словаря.

        :param query: Параметры фильтрации (например, courseId).
        :return: Список упражнений.
        """
        response = self.get_exercises_api(query)
        return GetExercisesResponseSchema.model_validate_json(response.text)

    def create_exercise(self, request: CreateExerciseRequestSchema) -> GetExerciseResponseSchema:
        """
        Создаёт новое упражнение и возвращает созданный объект.

        :param request: Данные для создания упражнения.
        :return: Данные созданного упражнения.
        """
        response = self.create_exercise_api(request)
        return GetExerciseResponseSchema.model_validate_json(response.text)

    def update_exercise(self, exercise_id: str, request: UpdateExerciseRequestSchema) -> GetExerciseResponseSchema:
        """
        Обновляет существующее упражнение и возвращает обновлённый объект.

        :param exercise_id: ID упражнения для обновления.
        :param request: Поля и значения для обновления.
        :return: Обновлённые данные упражнения.
        """
        response = self.update_exercise_api(exercise_id, request)
        return GetExerciseResponseSchema.model_validate_json(response.text)

def get_exercises_client(user: AuthenticationUserSchema) -> ExercisesClient:
    """Фабричная функция для создания экземпляра ExercisesClient с аутентификацией."""
    return ExercisesClient(client=get_private_http_client(user))
