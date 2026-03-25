from django import forms

from author.models import Author
from book.models import Book


# I created this form to handle both creating and editing books
class BookForm(forms.ModelForm):
    # I added this field separately because authors is a M2M relation, not a direct model field
    authors = forms.ModelMultipleChoiceField(
        queryset=Author.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Authors',
    )

    class Meta:
        model = Book
        fields = ['name', 'description', 'count']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Book title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Short description', 'rows': 3}),
            'count': forms.NumberInput(attrs={'min': 0}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # I pre-populate the authors field when editing an existing book
        if self.instance and self.instance.pk:
            self.fields['authors'].initial = self.instance.authors.all()

    def save(self, commit=True):
        book = super().save(commit=commit)
        if commit:
            # I use .set() here so it properly replaces all author relations
            book.authors.set(self.cleaned_data.get('authors', []))
        return book
