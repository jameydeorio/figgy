# encoding: utf-8
'''
Copyright (c) 2013 Safari Books Online. All rights reserved.
'''

import uuid

from django.test import TestCase

from storage import models
from storage.models import Alias, Book


class TestModels(TestCase):
    def setUp(self):
        self.book = models.Book.objects.create(title="The Title", pk=str(uuid.uuid4()))
        self.book.aliases.create(scheme='ISBN-10', value='1234567890')

    def test_book_have_unicode_method(self):
        '''The Book should have a __unicode__ method.'''
        expected = 'Book {}'.format(self.book.title)
        self.assertEquals(expected, unicode(self.book))

    def test_get_book_by_isbn(self):
        self.assertEqual(self.book, Book.objects.get_by_isbn_10('1234567890'))
