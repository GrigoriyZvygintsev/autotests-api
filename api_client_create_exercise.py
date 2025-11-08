from clients.courses.courses_client import get_courses_client, CreateCourseRequestDict
from clients.exercises.exercises_client import get_exercises_client, CreateExerciseRequest
from clients.files.files_client import get_files_client, CreateFileRequestDict
from clients.private_http_builder import AuthenticationUserDict
from clients.users.public_users_client import get_public_users_client, CreateUserRequestDict
from tools.fakers import get_random_email, generate_password

public_users_client = get_public_users_client()

# Создаем пользователя
create_user_request = CreateUserRequestDict(
    email=get_random_email(),
    password=generate_password(),
    lastName="string",
    firstName="string",
    middleName="string"
)
create_user_response = public_users_client.create_user(create_user_request)

# Инициализируем клиенты
authentication_user = AuthenticationUserDict(
    email=create_user_request['email'],
    password=create_user_request['password']
)
files_client = get_files_client(authentication_user)
courses_client = get_courses_client(authentication_user)
exercises_client = get_exercises_client(authentication_user)

# Загружаем файл
create_file_request = CreateFileRequestDict(
    filename="kartinka_dlay_api_klienta.png",
    directory="courses",
    upload_file="./testdata/files/kartinka_dlay_api_klienta.png"
)
create_file_response = files_client.create_file(create_file_request)
print('Create file data:', create_file_response)

# Создаем курс
create_course_request = CreateCourseRequestDict(
    title="Python",
    maxScore=200,
    minScore=5,
    description="Python API course - 1.1",
    estimatedTime="4 weeks",
    previewFileId=create_file_response['file']['id'],
    createdByUserId=create_user_response['user']['id']
)
create_course_response = courses_client.create_course(create_course_request)
print('Create course data:', create_course_response)

create_exercise_request = CreateExerciseRequest(
    title="Python API client guide",
    courseId=create_course_response['course']['id'],
    maxScore=50,
    minScore=1,
    orderIndex=1,
    description="Python API exercise - 1.1",
    estimatedTime="1 weeks",
)

create_exercise_response = exercises_client.create_exercise(create_exercise_request)
print('Create exercise data:', create_exercise_response)