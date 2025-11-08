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