from config import settings
import sys
import platform

def create_allure_environment_file():
    os_info = f'os_info={platform.system()}, {platform.release()}'
    python_version = f'python_version={sys.version}'
    # Создаем список из элементов в формате {key}={value}
    items = [f'{key}={value}' for key, value in settings.model_dump().items()]
    items.extend([os_info, python_version])
    # Собираем все элементы в единую строку с переносами
    properties = '\n'.join(items)


    # Открываем файл ./allure-results/environment.properties на чтение
    with open(settings.allure_results_dir.joinpath('environment.properties'), 'w+') as file:
        file.write(properties)  # Записываем переменные в файл