# encoding: utf-8
# Created by David Rideout <drideout@safaribooksonline.com> on 2/7/14 4:58 PM
# Copyright (c) 2013 Safari Books Online, LLC. All rights reserved.
from django.db import IntegrityError
from termcolor import colored

from storage.models import Book
from storage.models import Alias


def process_book_element(book_element):
    """
    Process a book element into the database.

    :param book: book element
    :returns:
    """

    book, created = Book.objects.get_or_create(pk=book_element.get('id'))
    book.title = book_element.findtext('title')
    book.description = book_element.findtext('description')

    errors = []
    for alias in book_element.xpath('aliases/alias'):
        scheme = alias.get('scheme')
        value = alias.get('value')

        try:
            book.aliases.get_or_create(scheme=scheme, value=value)
        except IntegrityError, e:
            # tried to create alias, but value clashed with another book's alias
            existing_alias = Alias.objects.get(value=value)
            errors.append('Duplicate {} found on book "{}" with value {}'.format(scheme, existing_alias.book.id, value))

    if errors:
        print colored('"{}" not saved'.format(book.title), 'red')
        for error in errors:
            print colored(error, 'yellow')
        if created:
            book.delete()
    else:
        book.save()
        print colored('"{}" {}'.format(book.id, 'saved' if created else 'updated'), 'green')
