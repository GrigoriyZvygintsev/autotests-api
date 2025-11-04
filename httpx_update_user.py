import httpx
import time
import random
import string


# Генерация почты и пароля
def get_random_email():
    return f'test.{time.time()}@example.com'


def generate_password(length=8):
    # Буквы (верхний и нижний регистр) + цифры
    characters = string.ascii_letters + string.digits  # Пример: 'a-z, A-Z, 0-9'
    return ''.join(random.choice(characters) for _ in range(length))


random_email = get_random_email()
random_password = generate_password()

# Создание пользователя
body = {
    "email": random_email,
    "password": random_password,
    "lastName": "string",
    "firstName": "string",
    "middleName": "string"
}

response_creating_user = httpx.post('http://127.0.0.1:8000/api/v1/users', json=body)
user_id = response_creating_user.json()["user"]["id"]

print(f'Создан пользователь с id: {user_id}'
      f'\nпочтой: {random_email}'
      f'\nпаролем: {random_password} ')
print()

# Авторизация пользователя
body_authentication = {
    "email": random_email,
    "password": random_password
}

response_authentication = httpx.post('http://127.0.0.1:8000/api/v1/authentication/login',
                                     json=body_authentication)
accessToken = response_authentication.json()["token"]["accessToken"]
refreshToken = response_authentication.json()["token"]["refreshToken"]

print(f'пользователь авторизован и получен'
      f'\naccessToken: {accessToken}'
      f'\nrefreshToken: {refreshToken}')
print()

# Обновление данных о пользователе
user_headers = {
    "Authorization": f"Bearer {accessToken}"
}
body_patch = {
    "email": get_random_email(),
    "lastName": "VAAAXovich",
    "firstName": "Magregar",
    "middleName": "Magregorovich"
}
response_patch_user = httpx.patch(f'http://127.0.0.1:8000/api/v1/users/{user_id}', headers=user_headers,
                                  json=body_patch)
print(response_patch_user.json())
print(f'Данные обновлены о пользователе {response_patch_user.json()["user"]["firstName"]} '
      f'{response_patch_user.json()["user"]["middleName"]} '
      f'{response_patch_user.json()["user"]["lastName"]}')
print()

# Удаление пользователя - очистка тестовых данных
response_delite_user = httpx.delete(f'http://127.0.0.1:8000/api/v1/users/{user_id}', headers=user_headers)

if response_delite_user.json() is None:
    print(f'Пользователь c id-{user_id} удален успешно')
else:
    print('Пользователь не удален')
