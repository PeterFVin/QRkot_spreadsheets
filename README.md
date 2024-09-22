# Проект cat_charity_fund

## О проекте

Проект представляет собой благотворительный фонд, который собирает пожертвования на различные целевые проекты. Сумма, вносимая жертвователем, поочерёдно распределяется на открытые проекты.

### Использованные технологии: 

 - python==3.11.3
 - FastAPI
 - SQLAlchemy
 - Alembic
 - Pydantic
 - Asyncio

### Автор проекта:

Петр Виноградов, python plus, когорта 31+
[Петр Виноградов](https://github.com/PeterFVin)

### Как запустить проект:

Клонировать репозиторий:

git clone https://github.com/PeterFVin/cat_charity_fund.git
```
Перейти в папку cat_charity_fund
```
Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```
Сделать миграции
```
alembic upgrade head
```
Запустить проект:

```
uvicorn app.main:app --reload
```

### Документация к проекту:

[Swagger](http://127.0.0.1:8000/docs)
[Redoc](http://127.0.0.1:8000/redoc)
