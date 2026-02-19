from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from .models import Book, Genre
from django.db.models import Q
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def index (request):
    books = Book.objects.all()
    genres =Genre.objects.all()

    search_books = request.GET.get('search', '')
    if search_books:
        books = Book.objects.filter(
            Q(title__icontains=search_books) |
            Q(author__icontains=search_books)
        )

    genre_filter = request.GET.get('genre', '')
    if genre_filter:
        books= books.filter(genre_id=genre_filter)

    return render(request, 'index.html', {
        'books': books,
        'genres': genres,
        'search_books': search_books,
        'genre_filter': genre_filter})

def create(request):
    try:
        book = Book()
        if request.method == 'POST':
            book = Book()
            book.title = request.POST.get('title')
            book.author = request.POST.get('author')
            book.genre = request.POST.get('genre')
            book.isbn = request.POST.get('isbn')
            book.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'create.html', {"book": book})
    except Book.DoesNotExist:
        return HttpResponseNotFound("Книга не добавлена")

def edit(request, id):
    try:
        book = Book.objects.get(id=id)
        if request.method == 'POST':
            book.title = request.POST.get('title')
            book.author = request.POST.get('author')
            book.genre = request.POST.get('genre')
            book.isbn = request.POST.get('isbn')
            book.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'edit.html', {"book": book})
    except Book.DoesNotExist:
        return HttpResponseNotFound("Книга не найдена")

def delete(request, id):
    try:
        book = Book.objects.get(id=id)
        book.delete()
        return HttpResponseRedirect('/')
    except Book.DoesNotExist:
        return HttpResponseNotFound("Книга не найдена")

def login_view(request):

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
    return HttpResponseRedirect('/')