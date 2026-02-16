from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from .models import Book
from django.db.models import Q

def index (request):
    books = Book.objects.all()

    search_books = request.GET.get('search', '')
    if search_books:
        books = Book.objects.filter(
            Q(title__icontains=search_books) |
            Q(author__icontains=search_books)
        )

    return render(request, 'index.html', {
        'books': books,
        'search_books': search_books})

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
