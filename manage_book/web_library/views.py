from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from .models import Book, Genre, BookRequest, UserProfile
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone


@login_required(login_url='/login/')
def index(request):
    profile = UserProfile.objects.get(user=request.user)

    if profile.role == 'librarian':
        return librarian_dashboard(request)
    else:
        return reader_dashboard(request)


def librarian_dashboard(request):
    books = Book.objects.all()
    genres = Genre.objects.all()
    requests = BookRequest.objects.all().select_related('user', 'book')

    # Фильтрация для книг
    search_books = request.GET.get('search', '')
    if search_books:
        books = Book.objects.filter(
            Q(title__icontains=search_books) |
            Q(author__icontains=search_books)
        )

    genre_filter = request.GET.get('genre', '')
    if genre_filter:
        books = books.filter(genre_id=genre_filter)

    # Фильтрация для запросов
    request_status = request.GET.get('request_status', '')
    if request_status:
        requests = requests.filter(status=request_status)

    return render(request, 'librarian_dashboard.html', {
        'books': books,
        'genres': genres,
        'requests': requests,
        'search_books': search_books,
        'genre_filter': genre_filter,
        'request_status': request_status,
    })


def reader_dashboard(request):
    profile = UserProfile.objects.get(user=request.user)
    books = Book.objects.filter(available=True)
    genres = Genre.objects.all()
    user_requests = BookRequest.objects.filter(user=request.user)

    # Фильтрация книг
    search_books = request.GET.get('search', '')
    if search_books:
        books = Book.objects.filter(
            Q(title__icontains=search_books) |
            Q(author__icontains=search_books),
            available=True
        )

    genre_filter = request.GET.get('genre', '')
    if genre_filter:
        books = books.filter(genre_id=genre_filter)

    return render(request, 'reader_dashboard.html', {
        'books': books,
        'genres': genres,
        'user_requests': user_requests,
        'search_books': search_books,
        'genre_filter': genre_filter,
        'profile': profile,
    })


@login_required(login_url='/login/')
def create_book(request):
    if not is_librarian(request.user):
        messages.error(request, 'У вас нет прав для добавления книг')
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        genre_id = request.POST.get('genre')
        isbn = request.POST.get('isbn')

        if title and author and genre_id:
            book = Book.objects.create(
                title=title,
                author=author,
                genre_id=genre_id,
                isbn=isbn
            )
            messages.success(request, f'Книга "{title}" успешно добавлена')
            return HttpResponseRedirect('/')

    genres = Genre.objects.all()
    return render(request, 'create.html', {'genres': genres})


@login_required(login_url='/login/')
def edit_book(request, id):
    if not is_librarian(request.user):
        messages.error(request, 'У вас нет прав для редактирования книг')
        return HttpResponseRedirect('/')

    try:
        book = Book.objects.get(id=id)
        if request.method == 'POST':
            book.title = request.POST.get('title')
            book.author = request.POST.get('author')
            book.genre_id = request.POST.get('genre')
            book.isbn = request.POST.get('isbn')
            book.available = request.POST.get('available') == 'on'
            book.save()
            messages.success(request, f'Книга "{book.title}" успешно обновлена')
            return HttpResponseRedirect('/')
        else:
            genres = Genre.objects.all()
            return render(request, 'edit.html', {"book": book, "genres": genres})
    except Book.DoesNotExist:
        return HttpResponseNotFound("Книга не найдена")


@login_required(login_url='/login/')
def delete_book(request, id):
    if not is_librarian(request.user):
        messages.error(request, 'У вас нет прав для удаления книг')
        return HttpResponseRedirect('/')

    try:
        book = Book.objects.get(id=id)
        book.delete()
        messages.success(request, f'Книга "{book.title}" успешно удалена')
        return HttpResponseRedirect('/')
    except Book.DoesNotExist:
        return HttpResponseNotFound("Книга не найдена")


@login_required(login_url='/login/')
def request_book(request, id):
    if is_librarian(request.user):
        messages.error(request, 'Библиотекари не могут запрашивать книги')
        return HttpResponseRedirect('/')

    try:
        book = Book.objects.get(id=id)
        if not book.available:
            messages.error(request, 'Эта книга недоступна')
            return HttpResponseRedirect('/')

        # Проверка на существующий активный запрос
        existing_request = BookRequest.objects.filter(
            user=request.user,
            book=book,
            status__in=['pending', 'approved']
        ).exists()

        if existing_request:
            messages.error(request, 'Вы уже запросили эту книгу')
        else:
            BookRequest.objects.create(user=request.user, book=book)
            messages.success(request, f'Запрос на книгу "{book.title}" отправлен')

        return HttpResponseRedirect('/')
    except Book.DoesNotExist:
        return HttpResponseNotFound("Книга не найдена")


@login_required(login_url='/login/')
def cancel_request(request, id):
    if is_librarian(request.user):
        messages.error(request, 'Библиотекари не могут отменять запросы')
        return HttpResponseRedirect('/')

    try:
        book_request = BookRequest.objects.get(id=id, user=request.user)
        if book_request.status == 'pending':
            book_request.delete()
            messages.success(request, 'Запрос отменен')
        else:
            messages.error(request, 'Нельзя отменить обработанный запрос')
        return HttpResponseRedirect('/')
    except BookRequest.DoesNotExist:
        return HttpResponseNotFound("Запрос не найден")


@login_required(login_url='/login/')
def process_request(request, id, action):
    if not is_librarian(request.user):
        messages.error(request, 'У вас нет прав для обработки запросов')
        return HttpResponseRedirect('/')

    try:
        book_request = BookRequest.objects.get(id=id)

        if action == 'approve':
            if book_request.book.available:
                book_request.status = 'approved'
                book_request.approved_date = timezone.now()
                book_request.book.available = False
                book_request.book.save()
                book_request.save()
                messages.success(request, f'Запрос на книгу "{book_request.book.title}" одобрен')
            else:
                messages.error(request, 'Книга уже недоступна')

        elif action == 'reject':
            book_request.status = 'rejected'
            book_request.save()
            messages.success(request, f'Запрос на книгу "{book_request.book.title}" отклонен')

        elif action == 'return':
            if book_request.status == 'approved':
                book_request.status = 'returned'
                book_request.return_date = timezone.now()
                book_request.book.available = True
                book_request.book.save()
                book_request.save()
                messages.success(request, f'Книга "{book_request.book.title}" возвращена')

        return HttpResponseRedirect('/')
    except BookRequest.DoesNotExist:
        return HttpResponseNotFound("Запрос не найден")


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'login.html', {'err': 'Неправильный логин или пароль'})

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def is_librarian(user):
    try:
        profile = UserProfile.objects.get(user=user)
        return profile.role == 'librarian'
    except UserProfile.DoesNotExist:
        return False


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, 'Пароли не совпадают')
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
            return render(request, 'register.html')

        user = User.objects.create_user(username=username, password=password)
        UserProfile.objects.create(user=user, role='reader')
        login(request, user)
        messages.success(request, 'Регистрация успешно завершена!')
        return HttpResponseRedirect('/')

    return render(request, 'register.html')