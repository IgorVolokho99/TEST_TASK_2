Требуется:

- Docker Compose

## Установка

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/yourusername/TEST_TASK_2.git
    cd TEST_TASK_2
    ```
2. Соберите и запустите контейнеры:

    ```bash
    docker-compose up --build
    ```

## Структура проекта

- `main.py`: Основной скрипт, который инициализирует базу данных и выполняет основные задачи.
- `database.py`: Содержит класс `Database` для взаимодействия с базой данных.
- `models.py`: Определяет модели данных для SQLAlchemy.
- `data.json`: JSON-файл с данными для загрузки в базу данных.