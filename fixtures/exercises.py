import pytest
from pydantic import BaseModel

from clients.exercises.exercises_client import get_exercises_client, ExercisesClient
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, GetExerciseResponseSchema, \
    GetExercisesResponseSchema, GetExercisesQuerySchema
from fixtures.courses import CourseFixture
from fixtures.users import UserFixture


class ExerciseFixture(BaseModel):
    request: CreateExerciseRequestSchema
    response: GetExerciseResponseSchema

class ExercisesFixtures(BaseModel):
    request: list[CreateExerciseRequestSchema]
    response: GetExercisesResponseSchema

@pytest.fixture
def exercises_client(function_user: UserFixture) -> ExercisesClient:
    return get_exercises_client(function_user.authentication_user)

@pytest.fixture
def function_exercise(
        exercises_client: ExercisesClient,
        function_course: CourseFixture
) -> ExerciseFixture:
    course_id = function_course.response.course.id
    request = CreateExerciseRequestSchema(course_id = course_id)
    response = exercises_client.create_exercise(request)
    return ExerciseFixture(request=request, response=response)

@pytest.fixture
def function_exercises(
    exercises_client: ExercisesClient,
    function_course: CourseFixture,
    amount: int = 2,
) -> ExercisesFixtures:
    """Создаёт несколько упражнений для курса и возвращает список упражнений для курса через get_exercises."""
    course_id = function_course.response.course.id
    requests = [CreateExerciseRequestSchema(course_id=course_id) for _ in range(amount)]

    for request in requests:
        exercises_client.create_exercise(request)

    response = exercises_client.get_exercises(GetExercisesQuerySchema(course_id=course_id))
    return ExercisesFixtures(requests=requests, response=response)



