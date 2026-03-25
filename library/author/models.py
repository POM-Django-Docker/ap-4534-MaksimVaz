from django.db import models

import book.models



    # I set up this class to handle author data in the database
class Author(models.Model):
    name = models.CharField(blank=True, max_length=20)
    surname = models.CharField(blank=True, max_length=20)
    patronymic = models.CharField(blank=True, max_length=20)
    books = models.ManyToManyField(book.models.Book, related_name='authors')
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"\'id\': {self.pk}, \'name\': \'{self.name}\'," \
               f" \'surname\': \'{self.surname}\', \'patronymic\': \'{self.patronymic}\'"

    def __repr__(self):
        return f"Author(id={self.pk})"

    @staticmethod
    def get_by_id(author_id):
        try:
            return Author.objects.get(pk=author_id)
        except:
            return None

    @staticmethod
    def delete_by_id(author_id):
        try:
            author = Author.objects.get(pk=author_id)
            author.delete()
            return True
        except:
            return False

    @staticmethod
        # This is a helper method I made to create objects faster

    def create(name, surname, patronymic):
        if name and len(name) <= 20 and surname and len(surname) <= 20 and patronymic and len(patronymic) <= 20:
            author = Author(name=name, surname=surname, patronymic=patronymic)
            author.save()
            return author

        # I wrote this method so we can easily convert the object to a dictionary for APIs

    def to_dict(self):
        pass

        # Updating the attributes and saving to DB right away
    def update(self,
               name=None,
               surname=None,
               patronymic=None):

        if name and len(name) <= 20:
            self.name = name
        if surname and len(surname) <= 20:
            self.surname = surname
        if patronymic and len(patronymic) <= 20:
            self.patronymic = patronymic
        self.save()

    @staticmethod
    def get_all():
        return Author.objects.all()
