![Main tests](https://github.com/licaro-1/foodgram-project-react/actions/workflows/foodgram_workflow.yaml/badge.svg)

```
Ознакомиться с API документацией проекта можно тут:
http://51.250.91.245/api/docs/

Ознакомиться с самим проектом:
http://51.250.91.245/

Данные от админ аккаунта:
Email: admin@gmail.com
admin
```

### Как запустить проект в контейнере:

Клонировать репозиторий и перейти в папку infra в командной строке:

```
SSH git clone git@github.com:licaro-1/foodgram-project-react.git

HTTPS git clone https://github.com/licaro-1/foodgram-project-react.git
```

```
cd foodgram-project-react/infra
```

Создать файл .env и заполнить его данными о БД.

Шаблон:

```
DB_ENGINE=django.db.backends.postgresql_psycopg2
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=  # пароль для подключения к БД (установите свой)
DB_HOST=db
DB_PORT=5432 # порт для подключения к БД
SECRET_KEY= #Код проекта
```

Запустить Докер через командную строку:

```
docker-compose up
```

Выполнить миграции, подгрузить статику и загрузить рецепты в базу данных:

```
sudo docker-compose exec backend python manage.py migrate
sudo docker-compose exec backend python manage.py collectstatic --no-input
sudo docker-compose exec backend python manage.py export_ingredients
```

#### Сервер запущен

