# encoding: utf-8
'''
Copyright (c) 2013 Safari Books Online. All rights reserved.
'''

import uuid

from django.test import TestCase

from storage import models
from storage.models import Alias, Book, Edition


class TestModels(TestCase):
    def setUp(self):
        self.book = models.Book.objects.create(title="The Title", pk=str(uuid.uuid4()))
        self.edition = self.book.editions.create(title=self.book.title, book=self.book)
        self.edition.aliases.create(scheme='ISBN-13', value='1234567890')

    def test_book_have_unicode_method(self):
        '''The Book should have a __unicode__ method.'''
        expected = 'Book {}'.format(self.book.title)
        self.assertEquals(expected, unicode(self.book))

    def test_get_or_create_by_isbn_13(self):
        self.assertEqual((self.edition, False, False), Edition.objects.get_or_create_by_isbn_13('1234567890', self.book.pk))
