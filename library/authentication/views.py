from django.contrib import messages
from django.shortcuts import redirect

from authentication.models import CustomUser
from library.helpers import get_current_user, librarian_required, login_user, logout_user, render_page


def register_view(request):
    if get_current_user(request):
        return redirect('home')

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        middle_name = request.POST.get('middle_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        role = 1 if request.POST.get('role') == '1' else 0

        if not first_name or not last_name or not email or not password:
            messages.error(request, 'Fill in the required fields.')
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'User with this email already exists.')
        else:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                middle_name=middle_name,
                email=email,
                role=role,
                is_active=True,
            )
            user.set_password(password)
            user.save()
            login_user(request, user)
            messages.success(request, 'Registration completed.')
            return redirect('home')

    return render_page(request, 'authentication/register.html')


def login_view(request):
    if get_current_user(request):
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        user = CustomUser.objects.filter(email=email).first()

        if not user or not user.check_password(password):
            messages.error(request, 'Wrong email or password.')
        elif not user.is_active:
            messages.error(request, 'This user is inactive.')
        else:
            login_user(request, user)
            messages.success(request, 'You are logged in.')
            return redirect('home')

    return render_page(request, 'authentication/login.html')


def logout_view(request):
    logout_user(request)
    messages.success(request, 'You are logged out.')
    return redirect('home')


@librarian_required
def users_list(request):
    users = CustomUser.objects.all().order_by('id')
    return render_page(request, 'authentication/users_list.html', {'users': users})


@librarian_required
def user_detail(request, user_id):
    user = CustomUser.objects.filter(id=user_id).first()
    if not user:
        messages.error(request, 'User not found.')
        return redirect('users_list')

    return render_page(request, 'authentication/user_detail.html', {'profile_user': user})
