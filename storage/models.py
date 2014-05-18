# encoding: utf-8

from django.db import models


class BaseModel(models.Model):
    '''Base class for all models'''
    created_time = models.DateTimeField('date created', auto_now_add=True)
    last_modified_time = models.DateTimeField('last-modified', auto_now=True, db_index=True)

    class Meta:
        abstract = True


class BookManager(models.Manager):
    def get_by_isbn_10(self, isbn_10):
        '''
        Get a book by its ISBN-10 code.

        :returns: a book or None
        '''
        try:
            return Book.objects.get(aliases__scheme='ISBN-10', aliases__value=isbn_10)
        except Book.DoesNotExist:
            return None


class Book(BaseModel):
    '''
    Main storage for a Book object.
    '''
    id = models.CharField(max_length=30, primary_key=True, help_text="The primary identifier of this title, we get this value from publishers.")
    title = models.CharField(max_length=128, help_text="The title of this book.", db_index=True, null=False, blank=False)
    description = models.TextField(blank=True, null=True, default=None, help_text="Very short description of this book.")
    objects = BookManager()

    def __unicode__(self):
        return u"Book %s" % self.title

    class Meta:
        ordering = ['title']


class Alias(BaseModel):
    '''
    A book can have one or more aliases which

    For example, a book can be referred to with an ISBN-10 (older, deprecated scheme), ISBN-13 (newer scheme),
    or any number of other aliases.
    '''
    book = models.ForeignKey(Book, related_name='aliases')
    value = models.CharField(max_length=255, db_index=True, unique=True, help_text="The value of this identifier")
    scheme = models.CharField(max_length=40, help_text="The scheme of identifier")

    def __unicode__(self):
        return '%s identifier for %s' % (self.scheme, self.book.title)

    @classmethod
    def get_probable_matches(cls, aliases):
        '''
        Finds the most probable matches for a book based on alias information, favoring a matching ISBN-10.

        :returns: the isbn-10 book match (or None) and a list of non-isbn-10 book matches
        '''
        isbn_10_match = None
        non_isbn_10_matches = []
        for alias in aliases:
            scheme = alias.get('scheme')
            value = alias.get('value')
            if scheme == 'ISBN-10':
                isbn_10_match = Book.objects.get_by_isbn_10(value)
            else:
                non_isbn_10_matches += Alias.objects.filter(scheme=scheme, value=value)

        return isbn_10_match, non_isbn_10_matches
