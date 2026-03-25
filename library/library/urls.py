from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from library.helpers import render_page
from author.api_views import AuthorViewSet
from authentication.api_views import UserViewSet

# Added DRF router
router = DefaultRouter()
router.register(r'author', AuthorViewSet, basename='author')
router.register(r'user', UserViewSet, basename='user')

def home(request):
    return render_page(request, 'home.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('auth/', include('authentication.urls')),
    path('books/', include('book.urls')),
    path('users/', include('authentication.urls_users')),
    path('orders/', include('order.urls')),
    path('authors/', include('author.urls')),
    # API routes
    path('api/v1/auth/', include('rest_framework.urls')),
    path('api/v1/', include(router.urls)),
]
