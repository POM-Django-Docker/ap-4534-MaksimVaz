from django.urls import path

from author import views

urlpatterns = [
    path('', views.authors_list, name='authors_list'),
    path('create/', views.author_create, name='author_create'),
    path('<int:author_id>/delete/', views.author_delete, name='author_delete'),
]
