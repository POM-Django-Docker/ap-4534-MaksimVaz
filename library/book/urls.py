from django.urls import path

from book import views

# I added create, edit and delete routes here for the librarian CRUD functionality
urlpatterns = [
    path('', views.books_list, name='books_list'),
    path('create/', views.book_create, name='book_create'),
    path('user/<int:user_id>/', views.user_books, name='user_books'),
    path('<int:book_id>/', views.book_detail, name='book_detail'),
    path('<int:book_id>/edit/', views.book_edit, name='book_edit'),
    path('<int:book_id>/delete/', views.book_delete, name='book_delete'),
]
