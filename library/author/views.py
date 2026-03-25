from django.contrib import messages
from django.shortcuts import redirect

from author.models import Author
from library.helpers import librarian_required, render_page


@librarian_required
def authors_list(request):
    authors = Author.objects.all().prefetch_related('books').order_by('id')
    return render_page(request, 'author/authors_list.html', {'authors': authors})


@librarian_required
def author_create(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        surname = request.POST.get('surname', '').strip()
        patronymic = request.POST.get('patronymic', '').strip()

        if not name or not surname or not patronymic:
            messages.error(request, 'Fill in all fields.')
        else:
            Author.objects.create(name=name, surname=surname, patronymic=patronymic)
            messages.success(request, 'Author created.')
            return redirect('authors_list')

    return render_page(request, 'author/author_create.html')


@librarian_required
def author_delete(request, author_id):
    if request.method != 'POST':
        return redirect('authors_list')

    author = Author.objects.filter(id=author_id).prefetch_related('books').first()
    if not author:
        messages.error(request, 'Author not found.')
    elif author.books.exists():
        messages.error(request, 'This author is attached to books.')
    else:
        author.delete()
        messages.success(request, 'Author deleted.')
    return redirect('authors_list')
