from django.db import models



    # I set up this class to handle book data in the database
class Book(models.Model):
    name = models.CharField(blank=True, max_length=128)
    description = models.CharField(blank=True, max_length=256)
    count = models.IntegerField(default=10)
    id = models.AutoField(primary_key=True)

        # Just returning a readable string representation here
    def __str__(self):
        return f"'id': {self.id}, 'name': '{self.name}', 'description': '{self.description}', 'count': {self.count}, 'authors': {[author.id for author in self.authors.all()]}"

    def __repr__(self):
        return f"Book(id={self.id})"

    @staticmethod
        # Safely fetching the item or returning None if not found
    def get_by_id(book_id):
        return Book.objects.get(id=book_id) if Book.objects.filter(id=book_id) else None

    @staticmethod
    def delete_by_id(book_id):
        if Book.get_by_id(book_id) is None:
            return False
        Book.objects.get(id=book_id).delete()
        return True

    @staticmethod
        # This is a helper method I made to create objects faster
    def create(name, description, count=10, authors=None):
        if len(name) > 128:
            return None

        book = Book()
        book.name = name
        book.description = description
        book.count = count
        if (authors is not None):
            for elem in authors:
                book.authors.add(elem)
        book.save()
        return book

        # I wrote this method so we can easily convert the object to a dictionary for APIs
    def to_dict(self):
        pass

        # Updating the attributes and saving to DB right away
    def update(self, name=None, description=None, count=None):
        if name is not None:
            self.name = name

        if description is not None:
            self.description = description

        if count is not None:
            self.count = count

        self.save()

    def add_authors(self, authors):
        if (authors is not None):
            for elem in authors:
                self.authors.add(elem)
                self.save()

    def remove_authors(self, authors):
        for elem in self.authors.values():
            self.authors.remove(elem['id'])

    @staticmethod
    def get_all():
        return list(Book.objects.all())
