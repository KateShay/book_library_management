import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manage_book.settings')
django.setup()

from django.contrib.auth.models import User
from web_library.models import Genre, Book, UserProfile, BookRequest


def create_test_data():
    print(" Начинаем создание тестовых данных...")

    # Создаем жанры
    genres_data = [
        "Художественная литература",
        "Научная литература",
        "Детектив",
        "Фантастика",
        "Поэзия",
        "Биография",
        "Психология",
        "История"
    ]

    genres = {}
    for genre_name in genres_data:
        genre, created = Genre.objects.get_or_create(name=genre_name)
        genres[genre_name] = genre
        if created:
            print(f"   Создан жанр: {genre_name}")

    # Создаем книги
    books_data = [
        {"title": "Мастер и Маргарита", "author": "Михаил Булгаков", "genre": "Художественная литература",
         "isbn": "978-5-699-12345-6"},
        {"title": "Преступление и наказание", "author": "Фёдор Достоевский", "genre": "Художественная литература",
         "isbn": "978-5-699-12346-3"},
        {"title": "1984", "author": "Джордж Оруэлл", "genre": "Фантастика", "isbn": "978-5-699-12347-0"},
        {"title": "Краткая история времени", "author": "Стивен Хокинг", "genre": "Научная литература",
         "isbn": "978-5-699-12348-7"},
        {"title": "Убийство в Восточном экспрессе", "author": "Агата Кристи", "genre": "Детектив",
         "isbn": "978-5-699-12349-4"},
        {"title": "Стив Джобс", "author": "Уолтер Айзексон", "genre": "Биография", "isbn": "978-5-699-12350-0"},
        {"title": "Думай медленно... решай быстро", "author": "Даниэль Канеман", "genre": "Психология",
         "isbn": "978-5-699-12351-7"},
        {"title": "Война и мир", "author": "Лев Толстой", "genre": "Художественная литература",
         "isbn": "978-5-699-12352-4"},
        {"title": "Гарри Поттер и философский камень", "author": "Джоан Роулинг", "genre": "Фантастика",
         "isbn": "978-5-699-12353-1"},
        {"title": "Сто лет одиночества", "author": "Габриэль Гарсиа Маркес", "genre": "Художественная литература",
         "isbn": "978-5-699-12354-8"},
        {"title": "Три товарища", "author": "Эрих Мария Ремарк", "genre": "Художественная литература",
         "isbn": "978-5-699-12355-5"},
        {"title": "451 градус по Фаренгейту", "author": "Рэй Брэдбери", "genre": "Фантастика",
         "isbn": "978-5-699-12356-2"},
        {"title": "Автостопом по галактике", "author": "Дуглас Адамс", "genre": "Фантастика",
         "isbn": "978-5-699-12357-9"},
        {"title": "Идиот", "author": "Фёдор Достоевский", "genre": "Художественная литература",
         "isbn": "978-5-699-12358-6"},
        {"title": "Тихий Дон", "author": "Михаил Шолохов", "genre": "Художественная литература",
         "isbn": "978-5-699-12359-3"},
    ]

    created_books = []
    for book_data in books_data:
        book, created = Book.objects.get_or_create(
            title=book_data["title"],
            defaults={
                "author": book_data["author"],
                "genre": genres[book_data["genre"]],
                "isbn": book_data["isbn"],
                "available": True
            }
        )
        created_books.append(book)
        if created:
            print(f"   Создана книга: {book.title}")

    # Создаем пользователей
    users_data = [
        {"username": "librarian", "password": "librarian123", "role": "librarian", "is_staff": True,
         "is_superuser": True},
        {"username": "ivan_reader", "password": "reader123", "role": "reader"},
        {"username": "maria_reader", "password": "reader123", "role": "reader"},
        {"username": "petr_reader", "password": "reader123", "role": "reader"},
        {"username": "anna_reader", "password": "reader123", "role": "reader"},
    ]

    users = {}
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data["username"],
            defaults={
                "password": user_data["password"],
                "is_staff": user_data.get("is_staff", False),
                "is_superuser": user_data.get("is_superuser", False),
                "email": f"{user_data['username']}@library.com"
            }
        )

        if created:
            user.set_password(user_data["password"])
            user.save()
            print(f"   Создан пользователь: {user.username}")

        # Создаем профиль
        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                "role": user_data["role"],
                "phone": f"+7-999-{user.id}",
                "address": f"г. Москва, ул. Читателей, д. {user.id}"
            }
        )
        if created:
            print(f"   Создан профиль для {user.username}: {profile.get_role_display()}")

        users[user.username] = user

    # Создаем несколько запросов на книги
    requests_data = [
        {"user": users["ivan_reader"], "book": created_books[0], "status": "pending"},
        {"user": users["ivan_reader"], "book": created_books[2], "status": "approved"},
        {"user": users["maria_reader"], "book": created_books[1], "status": "pending"},
        {"user": users["maria_reader"], "book": created_books[3], "status": "returned"},
        {"user": users["petr_reader"], "book": created_books[4], "status": "pending"},
        {"user": users["anna_reader"], "book": created_books[5], "status": "approved"},
    ]

    for req_data in requests_data:
        request, created = BookRequest.objects.get_or_create(
            user=req_data["user"],
            book=req_data["book"],
            defaults={
                "status": req_data["status"],
                "request_date": datetime.now()
            }
        )
        if created:
            print(f"   Создан запрос: {req_data['user'].username} -> {req_data['book'].title} ({req_data['status']})")

    # Статистика
    print("\n Статистика загруженных данных:")
    print(f"   Жанров: {Genre.objects.count()}")
    print(f"   Книг: {Book.objects.count()}")
    print(f"   Пользователей: {User.objects.count()}")
    print(f"   Профилей: {UserProfile.objects.count()}")
    print(f"   Запросов: {BookRequest.objects.count()}")

    print("\n Тестовые данные успешно загружены!")

    # Выводим информацию для входа
    print("\n Данные для входа:")
    print("  Библиотекарь: username: librarian, password: librarian123")
    print("  Читатели: username: ivan_reader, password: reader123")
    print("           username: maria_reader, password: reader123")
    print("           username: petr_reader, password: reader123")
    print("           username: anna_reader, password: reader123")


if __name__ == "__main__":
    create_test_data()