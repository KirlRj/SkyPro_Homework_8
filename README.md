
## Запуск проекта

1. Скопируй env.example в .env и заполни переменные:

   cp env.example .env

2. Запусти все сервисы:

   docker-compose up --build

3. Примени миграции (в отдельном терминале):

   docker-compose exec web python manage.py migrate

4. Приложение доступно на http://localhost:8000/

## Сервисы

- web — Django сервер (порт 8000)
- db — PostgreSQL (данные сохраняются в volume pg_data)
- redis — Redis брокер (данные сохраняются в volume redis_data)
- celery — воркер задач
- celery-beat — планировщик задач

## API документация

- Swagger: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/

## Остановка проекта

   docker-compose down

Для удаления данных (volumes):

   docker-compose down -v