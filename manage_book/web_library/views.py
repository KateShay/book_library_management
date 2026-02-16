import Q
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
