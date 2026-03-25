import datetime

from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone

from book.models import Book
from library.helpers import get_current_user, librarian_required, login_required, render_page
from order.forms import OrderCreateForm, OrderEditForm
from order.models import Order


@librarian_required
def orders_list(request):
    # I load book and user data in one query using select_related to avoid extra DB hits
    orders = Order.objects.select_related('book', 'user').order_by('-created_at')
    return render_page(request, 'order/orders_list.html', {'orders': orders, 'page_title': 'All orders'})


@login_required
def my_orders(request):
    current_user = get_current_user(request)
    # I reuse the same template as orders_list but filter by the logged-in user
    orders = Order.objects.filter(user=current_user).select_related('book', 'user').order_by('-created_at')
    return render_page(request, 'order/orders_list.html', {'orders': orders, 'page_title': 'My orders'})


@login_required
def order_create(request):
    current_user = get_current_user(request)
    # I block librarians here because only regular users should borrow books
    if current_user.role == 1:
        messages.error(request, 'Only ordinary users can create orders.')
        return redirect('orders_list')

    if request.method == 'POST':
        # I use OrderCreateForm so Django handles validation instead of doing it manually
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            book = form.cleaned_data['book']
            plated_end_at_date = form.cleaned_data['plated_end_at']
            # I combine the date with midnight time and make it timezone-aware
            plated_end_at = timezone.make_aware(
                datetime.datetime.combine(plated_end_at_date, datetime.time.min)
            )
            active_orders = Order.objects.filter(book=book, end_at__isnull=True).count()
            if active_orders >= book.count:
                messages.error(request, 'No available copies for this book.')
            else:
                Order.objects.create(user=current_user, book=book, plated_end_at=plated_end_at)
                messages.success(request, 'Order created.')
                return redirect('my_orders')
    else:
        form = OrderCreateForm()

    return render_page(request, 'order/order_form.html', {'form': form, 'form_title': 'Create order'})


@librarian_required
def order_edit(request, order_id):
    # I fetch the order with related data to display book/user info in the template
    order = Order.objects.filter(id=order_id).select_related('book', 'user').first()
    if not order:
        messages.error(request, 'Order not found.')
        return redirect('orders_list')

    if request.method == 'POST':
        form = OrderEditForm(request.POST)
        if form.is_valid():
            plated_end_at_date = form.cleaned_data['plated_end_at']
            plated_end_at = timezone.make_aware(
                datetime.datetime.combine(plated_end_at_date, datetime.time.min)
            )
            # I only update plated_end_at — the librarian shouldn't change other fields
            order.plated_end_at = plated_end_at
            order.save()
            messages.success(request, 'Order updated.')
            return redirect('orders_list')
    else:
        # I pre-fill the date field using the existing order's planned end date
        form = OrderEditForm(initial={'plated_end_at': order.plated_end_at.date()})

    return render_page(request, 'order/order_form.html', {
        'form': form,
        'form_title': f'Edit order #{order.id}',
        'order': order,
    })


@librarian_required
def close_order(request, order_id):
    # I only allow POST to prevent closing an order by visiting a URL directly
    if request.method != 'POST':
        return redirect('orders_list')

    order = Order.objects.filter(id=order_id).select_related('book', 'user').first()
    if not order:
        messages.error(request, 'Order not found.')
    elif order.end_at:
        messages.error(request, 'Order is already closed.')
    else:
        # I set end_at to now which marks the order as returned
        order.end_at = timezone.now()
        order.save()
        messages.success(request, 'Order closed.')
    return redirect('orders_list')
