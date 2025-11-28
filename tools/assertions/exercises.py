from clients.errors_schema import InternalErrorResponseSchema
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, GetExerciseResponseSchema, ExerciseSchema, \
    UpdateExerciseRequestSchema, UpdateExerciseResponseSchema, GetExercisesResponseSchema
from tools.assertions.base import assert_equal, assert_length
from tools.assertions.errors import assert_internal_error_response
import allure

@allure.step('Check create exercise response')
def assert_create_exercise_response(
        request: CreateExerciseRequestSchema,
        response: GetExerciseResponseSchema
):
    """
    Проверяет, соответствует ли ответ на создание упражнения данным запроса.

    :param request: Запрос на создание упражнения.
    :param response: Ответ API с данными созданного упражнения.
    :raises AssertionError: Если какое-либо из полей не совпадает.
    """
    assert_equal(request.title, response.exercise.title, "title")
    assert_equal(request.course_id, response.exercise.course_id, "course_id")
    assert_equal(request.max_score, response.exercise.max_score, "max_score")
    assert_equal(request.min_score, response.exercise.min_score, "min_score")
    assert_equal(request.order_index, response.exercise.order_index, "order_index")
    assert_equal(request.description, response.exercise.description, "description")
    assert_equal(request.estimated_time, response.exercise.estimated_time, "estimated_time")

@allure.step('Check exercise')
def assert_exercise(actual: ExerciseSchema, expected: ExerciseSchema):
    """
    Проверяет, что фактические данные упражнения соответствуют ожидаемым.

    :param actual: Фактические данные упражнения.
    :param expected: Ожидаемые данные упражнения.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    assert_equal(actual.title, expected.title, "title")
    assert_equal(actual.course_id, expected.course_id, "course_id")
    assert_equal(actual.max_score, expected.max_score, "max_score")
    assert_equal(actual.min_score, expected.min_score, "min_score")
    assert_equal(actual.order_index, expected.order_index, "order_index")
    assert_equal(actual.description, expected.description, "description")
    assert_equal(actual.estimated_time, expected.estimated_time, "estimated_time")

@allure.step('Check get exercise response')
def assert_get_exercise_response(
        get_exercise_response: GetExerciseResponseSchema,
        create_exercise_response: GetExerciseResponseSchema
):
    """
    Проверяет, что ответ на получение упражнения совпадает с данными созданного упражнения.

    :param get_exercise_response: Ответ API на GET /api/v1/exercises/{exercise_id}.
    :param create_exercise_response: Ответ API на создание этого упражнения.
    :raises AssertionError: Если какие-либо поля не совпадают.
    """
    assert_exercise(get_exercise_response.exercise, create_exercise_response.exercise)

@allure.step('Check update exercise response')
def assert_update_exercise_response(
        request: UpdateExerciseRequestSchema,
        response: UpdateExerciseResponseSchema
):
    """
    Проверяет, что тело ответа соответствует запросу на обновление задания.

    :param request: Запрос на обновление упражнения.
    :param response: Ответ API с данными обновленного упражнения.
    :raises AssertionError: Если какое-либо из полей не совпадает.
    """
    assert_equal(request.title, response.exercise.title, "title")
    assert_equal(request.max_score, response.exercise.max_score, "max_score")
    assert_equal(request.min_score, response.exercise.min_score, "min_score")
    assert_equal(request.order_index, response.exercise.order_index, "order_index")
    assert_equal(request.description, response.exercise.description, "description")
    assert_equal(request.estimated_time, response.exercise.estimated_time, "estimated_time")

@allure.step('Check exercise not found response')
def assert_exercise_not_found_response(actual: InternalErrorResponseSchema):
    """
    Проверяет, что ответ на запрос удаленного файла будет соответствовать ожидаемой ошибки.

    :param actual: Ответ от API с ошибкой валидации, который необходимо проверить.
    :raises AssertionError: Если фактический ответ не соответствует ожидаемому.
    """
    expected = InternalErrorResponseSchema(detail="Exercise not found")
    assert_internal_error_response(actual, expected)

@allure.step('Check get exercises response')
def assert_get_exercises_response(
        get_exercises_response: GetExercisesResponseSchema,
        create_exercise_responses: list[GetExerciseResponseSchema],
) -> None:
    """
    Проверяет, что ответ на получение списка упражнений
    содержит все ранее созданные упражнения.

    :param get_exercises_response: Ответ API на GET /api/v1/exercises.
    :param create_exercise_responses: Список ответов API на создание упражнений.
    :raises AssertionError: Если список упражнений или поля не совпадают.
    """
    assert_length(get_exercises_response.exercises, create_exercise_responses, "exercises")

    for index, create_exercise_response in enumerate(create_exercise_responses):
        assert_exercise(
            get_exercises_response.exercises[index],
            create_exercise_response.exercise,
        )