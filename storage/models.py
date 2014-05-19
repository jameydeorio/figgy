# encoding: utf-8

from django.db import models
from django.db.models import Max


class BaseModel(models.Model):
    """
    Base class for all models
    """
    created_time = models.DateTimeField('date created', auto_now_add=True)
    last_modified_time = models.DateTimeField('last-modified', auto_now=True, db_index=True)

    class Meta:
        abstract = True


class Book(BaseModel):
    """
    Main storage for a Book object.
    """
    id = models.CharField(max_length=30, primary_key=True,
                          help_text="The primary identifier of this title, we get this value from publishers.")
    title = models.CharField(max_length=128, help_text="The title of this book.", db_index=True, null=False,
                             blank=False)
    description = models.TextField(blank=True, null=True, default=None,
                                   help_text="Very short description of this book.")

    def __unicode__(self):
        return u"Book %s" % self.title

    class Meta:
        ordering = ['title']

    def get_next_edition_number(self):
        highest = self.editions.all().aggregate(highest=Max('edition_number'))['highest']
        if highest:
            return highest + 1
        else:
            return 1


class EditionManager(models.Manager):
    def get_or_create_by_isbn_13(self, isbn_13, book_id):
        """
        Get an edition by its ISBN-13 code.
        :returns: edition, edition_created, book_created
        """
        try:
            return Edition.objects.get(aliases__scheme='ISBN-13', aliases__value=isbn_13), False, False
        except Edition.DoesNotExist:
            book, book_created = Book.objects.get_or_create(pk=book_id)
            return Edition.objects.create(book=book), True, book_created


class Edition(BaseModel):
    """
    Editions hold the unique information for an edition of a book, like aliases and new titles.
    """
    book = models.ForeignKey(Book, related_name='editions')
    title = models.CharField(max_length=128, help_text="The title of this book.", db_index=True, null=False,
                             blank=False)
    description = models.TextField(blank=True, null=True, default=None,
                                   help_text="Very short description of this book.")
    edition_number = models.IntegerField(blank=True, null=True)
    objects = EditionManager()

    def __unicode__(self):
        return u"Edition {} of book '{}'".format(self.edition_number, self.book.title)


class Alias(BaseModel):
    """
    A book can have one or more aliases which

    For example, a book can be referred to with an ISBN-10 (older, deprecated scheme), ISBN-13 (newer scheme),
    or any number of other aliases.
    """
    edition = models.ForeignKey(Edition, null=True, related_name='aliases')
    value = models.CharField(max_length=255, db_index=True, unique=True, help_text="The value of this identifier")
    scheme = models.CharField(max_length=40, help_text="The scheme of identifier")

    def __unicode__(self):
        return '%s identifier for %s' % (self.scheme, self.edition.title)
