# Автоматизированные API‑тесты для учебного сервера

Учебный проект по автоматизированному тестированию REST API учебного сервера курса
["QA Automation Engineer API Course"](https://github.com/Nikita-Filonov/qa-automation-engineer-api-course).
Репозиторий содержит набор автотестов на Python и вспомогательные утилиты,
оформленные в стиле, близком к продакшен‑проектам.

Тестовое приложение, для которого пишутся проверки, опубликовано отдельно:
[API Course Test Server](https://github.com/Nikita-Filonov/qa-automation-engineer-api-course).

## Описание проекта

Цель проекта — автоматизировать проверку REST API учебного сервера:
авторизация, управление пользователями, курсами, заданиями и файлами.
Тесты проверяют корректность бизнес‑логики, контрактов API и обрабатывают как позитивные,
так и негативные сценарии.

Проект сфокусирован на качественной архитектуре автотестов и включает:

- слой API‑клиентов для структурированного доступа к эндпоинтам (`clients/`);
- набор `pytest`‑фикстур для переиспользования и удобной подготовки данных (`fixtures/`);
- конфигурацию на основе `pydantic` и `.env` (`config.py`, `.env`);
- строгую валидацию схем и данных;
- генерацию тестовых данных через `Faker`;
- интеграцию с Allure для наглядных отчётов;
- сбор покрытия API с помощью `swagger-coverage-tool`;
- параллельный запуск тестов и повторный прогон нестабильных кейсов.

## Стек технологий

- **Python** — язык реализации тестов.
- **Pytest** — тестовый фреймворк и система фикстур.
- **Allure** (`allure-pytest`) — сбор и визуализация отчётов о прохождении тестов.
- **HTTPX** — HTTP‑клиент для реализации API‑клиентов и хуков.
- **Pydantic / pydantic-settings** — типобезопасные модели и конфигурация через `.env`.
- **Faker** — генерация реалистичных тестовых данных.
- **pytest-xdist** — параллельный запуск тестов.
- **pytest-rerunfailures** — повторный запуск нестабильных тестов.
- **swagger-coverage-tool** — оценка покрытия API на основе фактических запросов.

## Структура проекта

Ключевые элементы репозитория:

- `clients/` — общий HTTP‑клиент и доменные клиенты (аутентификация, пользователи, курсы, задания, файлы),
  обработка ошибок, event hooks и вспомогательные функции.
- `tests/` — автотесты, организованные по доменам (`authentication`, `users`, `courses`, `exercises`, `files`),
  с использованием `pytest`‑маркеров (`regression`, `users`, `files`, `authentication`, `courses`, `exercises`).
- `fixtures/` — общие фикстуры для подготовки данных, авторизации и интеграции с Allure.
- `tools/` — вспомогательные утилиты: генераторы данных (`fakers`), логгер, кастомные ассерты и HTTP‑хелперы.
- `testdata/` — статические тестовые данные (например, файлы для проверки файлового API).
- `allure-results/` — директория с сырыми результатами Allure‑прогона.
- `coverage-results/` — результаты `swagger-coverage-tool` и история покрытий.
- `config.py` — центральная точка конфигурации (Pydantic Settings, чтение `.env`, подготовка директории Allure).
- `.env` — локальные настройки HTTP‑клиента и параметров `swagger-coverage-tool`.
- `.github/workflows/tests.yml` — GitHub Actions workflow для прогонов тестов в CI,
  генерации Allure‑отчёта и публикации результатов.

## Требования

- Python **3.12** (используется в CI);
- Git;
- установленный `Allure` CLI (для локального просмотра отчётов);
- запущенный тестовый сервер
  [API Course Test Server](https://github.com/Nikita-Filonov/qa-automation-engineer-api-course)
  на `http://localhost:8000`.

## Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/GrigoriyZvygintsev/autotests-api
cd autotests-api
```

### 2. Создание виртуального окружения

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Установка зависимостей

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Настройка окружения

Основные параметры конфигурации хранятся в `.env` и читаются через `pydantic-settings`:

- путь к тестовым данным (например, `TEST_DATA.IMAGE_PNG_FILE`);
- базовый URL и таймауты HTTP‑клиента (`HTTP_CLIENT.URL`, `HTTP_CLIENT.TIMEOUT`);
- параметры `swagger-coverage-tool` (описание сервисов, директории для результатов и истории).

При необходимости значения можно изменить под своё окружение.

## Запуск тестового сервера

Тесты ожидают, что учебный сервер будет доступен по `http://localhost:8000`.
Минимальный пример локального запуска (детали см. в README сервера):

```bash
git clone https://github.com/Nikita-Filonov/qa-automation-engineer-api-course
cd qa-automation-engineer-api-course
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

После запуска сервера вернитесь в директорию с автотестами.

## Запуск тестов

### Базовый прогон

```bash
pytest
```

### Регрессионный прогон с генерацией Allure‑результатов

```bash
pytest -m regression --alluredir=allure-results
```

Для запуска отдельных групп тестов можно использовать маркеры, например:

```bash
pytest -m users
pytest -m files
pytest -m authentication
```

### Параллельный запуск

Благодаря `pytest-xdist` тесты можно запускать параллельно (пример: 2 воркера):

```bash
pytest -m regression --alluredir=allure-results --numprocesses=2
```

## Allure‑отчёт

После прогона тестов с параметром `--alluredir` можно локально поднять Allure‑отчёт:

```bash
allure serve allure-results
```

Команда соберёт отчёт и откроет его в браузере.

## Покрытие API (Swagger Coverage)

В проекте настроен сбор покрытия API на основе фактически выполненных запросов.
Конфигурация задаётся через переменные `SWAGGER_COVERAGE_*` в `.env`.

После выполнения тестов отчёт о покрытии можно сгенерировать командой:

```bash
swagger-coverage-tool save-report
```

Результат сохраняется в файлы JSON/HTML (пути задаются в `.env`), а история покрытий
используется как локально, так и в CI.

## CI/CD (GitHub Actions)

Файл `.github/workflows/tests.yml` описывает пайплайн, который:

- запускается при `push` и `pull_request` в ветку `main`;
- поднимает учебный API‑сервер;
- устанавливает зависимости проекта;
- выполняет регрессионные тесты с генерацией результатов Allure и покрытия API;
- сохраняет историю покрытия и HTML‑отчёт как артефакты;
- собирает и публикует Allure‑отчёт в ветку `gh-pages` (GitHub Pages).

Таким образом, репозиторий демонстрирует полный цикл работы с автотестами:
от локальной разработки и настройки окружения до интеграции с CI и публикации отчётов.
