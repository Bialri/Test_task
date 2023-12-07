<h1>Инструкция по запуску</h1>

```shell
git clone https://github.com/Bialri/Test_task.git
```

Установка зависимостей

```shell
pip install -r requirements.txt
```

Необходимо создать файлы, хранящие переменных окружения
<p>Файл конфигурации для базы данных</p>

```shell
mkdir docker && touch docker/.env.db
```
Пример файла конфигурации базы данных

```dotenv
POSTGRES_DB=db
POSTGRES_USER=user
POSTGRES_PASSWORD=PASSWORD
```

Файл конфигурации Django

```shell
touch test_task/.env
```

Пример файла конфигурации Django

```dotenv
SECRET_KEY="SECRET"
DEBUG=True
#DATABASE
DB_ENGINE=django.db.backends.postgresql
DB_NAME=db
DB_USER=user
DB_PASSWORD=PASSWORD
DB_HOST=localhost
DB_PORT=5432

LANGUAGE_CODE=en-us
TIME_ZONE=UTC
STATIC_URL=static/
DEFAULT_AUTO_FIELD=django.db.models.BigAutoField
```
Требуемые поля: поля конфигурации базы данных, при отстутсвии остальных запуск возможен.

<p>Запуск контейнера с базой данных</p>

```shell
docker-compose up -d
```

<p>Применение миграций</p>

```shell
python3 manage.py makemigrations && python3 manage.py migrate
```

<p>Запуск dev сервера</p>

```shell
python3 manage.py runserver
```

<h2>Запуск тестов</h2>
 для запуска тестов требуется работающий контейнер базы данных

```shell
python3 manage.py test
```