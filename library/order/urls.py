from django.urls import path

from order import views

# I added the edit route so librarians can update the planned return date
urlpatterns = [
    path('', views.orders_list, name='orders_list'),
    path('my/', views.my_orders, name='my_orders'),
    path('create/', views.order_create, name='order_create'),
    path('<int:order_id>/edit/', views.order_edit, name='order_edit'),
    path('<int:order_id>/close/', views.close_order, name='close_order'),
]
