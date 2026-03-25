from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect

from authentication.models import CustomUser
from book.forms import BookForm
from book.models import Book
from library.helpers import librarian_required, login_required, render_page
from order.models import Order


@login_required
def books_list(request):
    # I load all books with their authors in one query to avoid N+1
    books = Book.objects.all().prefetch_related('authors').order_by('id')
    query = request.GET.get('q', '').strip()

    if query:
        # I search across name, description and all author name fields
        books = books.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(authors__name__icontains=query)
            | Q(authors__surname__icontains=query)
            | Q(authors__patronymic__icontains=query)
        ).distinct()

    return render_page(request, 'book/books_list.html', {'books': books, 'query': query})


@login_required
def book_detail(request, book_id):
    book = Book.objects.filter(id=book_id).prefetch_related('authors').first()
    if not book:
        messages.error(request, 'Book not found.')
        return redirect('books_list')

    # I calculate available copies by subtracting active (not returned) orders
    active_orders = Order.objects.filter(book=book, end_at__isnull=True).count()
    available_count = max(book.count - active_orders, 0)

    return render_page(
        request,
        'book/book_detail.html',
        {'book': book, 'available_count': available_count},
    )


@librarian_required
def book_create(request):
    # I handle both GET (show form) and POST (save book) in the same view
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book created.')
            return redirect('books_list')
    else:
        form = BookForm()
    return render_page(request, 'book/book_form.html', {'form': form, 'form_title': 'Add book'})


@librarian_required
def book_edit(request, book_id):
    book = Book.objects.filter(id=book_id).prefetch_related('authors').first()
    if not book:
        messages.error(request, 'Book not found.')
        return redirect('books_list')

    if request.method == 'POST':
        # I pass the existing book instance so the form knows it's an update, not a new record
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated.')
            return redirect('book_detail', book_id=book.id)
    else:
        # I pre-fill the form with current book data on GET
        form = BookForm(instance=book)

    return render_page(request, 'book/book_form.html', {'form': form, 'form_title': f'Edit: {book.name}', 'book': book})


@librarian_required
def book_delete(request, book_id):
    # I only allow deletion via POST to prevent accidental deletes from a link click
    if request.method != 'POST':
        return redirect('book_detail', book_id=book_id)
    book = Book.objects.filter(id=book_id).first()
    if book:
        book.delete()
        messages.success(request, 'Book deleted.')
    else:
        messages.error(request, 'Book not found.')
    return redirect('books_list')


@librarian_required
def user_books(request, user_id):
    user = CustomUser.objects.filter(id=user_id).first()
    if not user:
        messages.error(request, 'User not found.')
        return redirect('users_list')

    orders = Order.objects.filter(user_id=user_id).select_related('book', 'user').order_by('-created_at')
    return render_page(request, 'book/user_books.html', {'profile_user': user, 'orders': orders})
