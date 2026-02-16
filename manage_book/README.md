# Менеджер книг

Данная программа помогает в управлении библиотекой книг. Книги можно добавлять, редактировать, удалять. Поиск поможет найти необходимую книгу.

## Начало работы

Откройте терминал (командную строку) и выполните:

Шаг 1: Клонируйте репозиторий
- git clone https://github.com/KateShay/book_library_management
- cd django-library-management

Шаг 2: Создайте виртуальное окружение
На Windows:
- python -m venv env
- env\Scripts\activate

На macOS/Linux:
- python3 -m venv env
- source env/bin/activate

Шаг 3: Установите зависимости
- pip install -r requirements.txt

Шаг 4: Выполните миграции базы данных
- python manage.py migrate

Шаг 5: Запустите сервер
- python manage.py runserver

Шаг 6: Откройте приложение в браузере
- Перейдите по адресу: http://127.0.0.1:8000/
- Для входа в админ-панель: http://127.0.0.1:8000/admin/ (используйте данные суперпользователя)

Эти инструкции предоставят вам копию проекта и помогут запустить на вашем локальном компьютере для разработки и тестирования.

## Авторы

* **Екатерина Шатская**  - [KateShay](https://github.com/KateShay)

See also the list of [contributors](https://github.com/KateShay/book_library_management) who participated in this project.
