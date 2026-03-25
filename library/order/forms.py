from django import forms

from book.models import Book


# I made this form so regular users can create orders by picking a book and a date
class OrderCreateForm(forms.Form):
    book = forms.ModelChoiceField(
        queryset=Book.objects.all().order_by('name'),
        empty_label='Select a book',
        label='Book',
    )
    plated_end_at = forms.DateField(
        # I set the widget to type="date" so the browser shows a date picker
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Planned return date',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # I refresh the queryset in __init__ to get the latest books each time
        self.fields['book'].queryset = Book.objects.all().order_by('name')


# I made a separate form for editing because librarians only change the planned return date
class OrderEditForm(forms.Form):
    plated_end_at = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Planned return date',
    )
