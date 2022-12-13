# Развертывание на локальной машине
1. Создаем виртуальное окружение: python3 -m venv flask_venv
1. Активируем venv: source flask_venv/bin/activate
1. Устанавливаем зависимости: pip install -r requirements.txt
1. Создаем локальную БД: flask db upgrade

# Миграции
1. Активировать миграции: flask db init
1. Создать миграцию: flask db migrate -m "comment"
1. Применить миграции: flask db upgrade

# Автотесты

1. Запуск: pytest -v tests

# Чек-лист проекта

|      Complete      | [Priority](#Priority) |             Auth             | Task                                                                    | Url                                                        |
|:------------------:|:----------------------|:----------------------------:|:------------------------------------------------------------------------|:-----------------------------------------------------------|
|                    |                       |                              | **USER**                                                                |                                                            |
| :heavy_check_mark: | Base                  |                              | [Регистрация пользователя](#Регистрация-пользователя)                   | POST: /users                                               |
| :heavy_check_mark: | Base                  |                              | Список пользователей                                                    | GET: /users                                                |
| :heavy_check_mark: | Base                  |                              | Пользователь по id                                                      | GET: /users/{id}                                           |
|        :x:         | Medium                | ![fa-crown](icons/lock.png)  | [Авторизация пользователя](#Авторизация-пользователя)                   | GET: /auth/token                                           |
|        :x:         | High                  | ![fa-crown](icons/lock.png)  | Редактирование пользователя                                             | PUT: /users/{id}                                           |
|        :x:         | Medium                | ![fa-crown](icons/lock.png)  | Удаление пользователя                                                   | DELETE: /users/{id}                                        |
|                    |                       |                              | **NOTE**                                                                |                                                            |
| :heavy_check_mark: | Base                  | ![fa-crown](icons/lock.png)  | [Создание заметки](#Создание-заметки)                                   | POST: /notes                                               |
| :heavy_check_mark: | Base                  | ![fa-crown](icons/lock.png)  | [Список заметок](#Список-заметок)                                       | GET: /notes                                                |
| :heavy_check_mark: | Base                  | ![fa-crown](icons/lock.png)  | [Заметка по id](#Заметка-по-id)                                         | GET: /notes/{id}                                           |
|        :x:         | Medium                |                              | [Список всех публичных заметок](#Список-всех-публичных-заметок)         | GET: /notes/public                                         |
|        :x:         | Medium                | ![fa-crown](icons/lock.png)  | [Список заметок по имени тега](#Список-заметок-по-определенни-тега)     | GET: /notes/filter?tag=<tag_name>                          |
|        :x:         | Low                   |                              | [Публичные заметки по имени автора](#Публичные-заметки-по-имени-автора) | GET: /notes/filter?username=<username>                     |
|        :x:         | High                  | ![fa-crown](icons/lock.png)  | Редактирование заметки                                                  | PUT: /notes/{id}                                           |
| :heavy_check_mark: | Medium                | ![fa-crown](icons/lock.png)  | ~~Удаление заметки~~ Архивирование заметки                              | DELETE: /notes/{id}                                        |
| :heavy_check_mark: | Medium                | ![fa-crown](icons/lock.png)  | Восстановление заметки из архива                                        | PUT: ???                                                   |
| :heavy_check_mark: | Medium                | ![fa-crown](icons/lock.png)  | Просмотр архивных заметок                                               | GET: ???                                                   |
| :heavy_check_mark: | Base                  | ![fa-crown](icons/lock.png)  | [Добавление тегов заметке](#-Добавление-тегов-к-заметке)                | PUT: /notes/<note_id>/tags \ body: {“tags”: [id1, id2]}    |
|        :x:         | Medium                | ![fa-crown](icons/lock.png)  | Удаление тегов с заметок                                                | DELETE: /notes/<note_id>/tags \ body: {“tags”: [id1, id2]} |

|                    |                       |                              | **TAG**                                                                 |                                                            |
| :heavy_check_mark: | Base                  |                              | Создание тега                                                           | POST: /tags                                                |
| :heavy_check_mark: | Base                  |                              | Список всех тегов                                                       | GET: /tags                                                 |
|        :x:         | High                  |                              | Редактирование тега                                                     | PUT: /tags/{id}                                            |
| :heavy_check_mark: | Medium                |                              | Удаление тега                                                           | DELETE: /tags/{id}                                         |

## Регистрация пользователя

Создание нового пользователя в БД.

## Авторизация пользователя

Получение токена авторизации (Bearer Token)

## Создание заметки

Каждая заметка привязывается к конкретному пользователю.

## Список заметок

Пользователь должен видеть только заметки созданные им и публичные заметки других пользователей.

## Заметка по id

По id можно получить только свои заметки или публичные заметки созданные другими пользователями.

## Список всех публичных заметок

Получает список всех публичных заметок всех пользователей.

## Список заметок по определенни тега

Теперь заметки можно фильтровать по прикрепленным к ним тегам. \
Если указано имя несуществующего тега, то возвращаем пустой список, т.е. заметки с таким тегом не найдены.

## Публичные заметки по имени автора

Возвращаем все публичные заметки автором с указанным username. \
Если автор с указанным username не существует, возвращаем пустой список.

## Редактирование заметки

Изменение текста заметки и ее статуса(публичная/частная). Пользователь может редактировать только свои заметки.

## Удаление заметки

Удаление заметки из базы. Пользователь может удалять только свои заметки.

## Создание тегов

Можно создать теги(метки, хештеги). Затем каждый тег(или несколько тегов) можно назначить заметке. Теги дают возможность
удобной фильтрации заметок.

## Добавление тегов к заметке

Каждой метке можно назначить любое кол-во тегов.
Теги дают возможность удобной фильтрации заметок.

## Редактирование тега

Изменение названия тега.

## Удаление тега

Удаление тега из базы.

## Priority

Таблица приоритетов: чем выше приоритет в списке, тем задача важнее.

| Priority | Description                                                                                                                               | 
|:--------:|:------------------------------------------------------------------------------------------------------------------------------------------|
|   Base   | Самые важные задачи, без которых невозможно продолжать курс                                                                               |
|   High   | Задачи с высоким приоритетом, их рекомендуется выполнять в первую очередь                                                                 |
|  Medium  | Задачи со средним приоритетом, их рекомендуется выполнять когда нет задач с более высокими приоритетами                                   |
|   Low    | Дополнительные задачи с низким приоритетом, их рекомендуется выполнять в самый последний момент./ Часто - это задачи повышенной сложности |