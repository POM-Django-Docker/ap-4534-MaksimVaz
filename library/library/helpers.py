from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect, render

from authentication.models import CustomUser


def get_current_user(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return None
    return CustomUser.objects.filter(id=user_id, is_active=True).first()


def render_page(request, template_name, context=None, status=200):
    context = context or {}
    context['current_user'] = get_current_user(request)
    return render(request, template_name, context, status=status)


def login_user(request, user):
    request.session['user_id'] = user.id


def logout_user(request):
    request.session.pop('user_id', None)


def login_required(view_func):
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        if not get_current_user(request):
            messages.error(request, 'Please log in first.')
            return redirect('login')
        return view_func(request, *args, **kwargs)

    return wrapped


def librarian_required(view_func):
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        user = get_current_user(request)
        if not user:
            messages.error(request, 'Please log in first.')
            return redirect('login')
        if user.role != 1:
            messages.error(request, 'This page is only for librarians.')
            return redirect('home')
        return view_func(request, *args, **kwargs)

    return wrapped
