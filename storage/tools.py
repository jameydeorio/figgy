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
    book, book_created = Book.objects.get_or_create(pk=book_element.get('id'))
    book.title = book_element.findtext('title')
    book.description = book_element.findtext('description')

    errors = []
    aliases = [alias for alias in book_element.xpath('aliases/alias')]
    created_aliases = []
    for alias in aliases:
        scheme = alias.get('scheme')
        value = alias.get('value')
        try:
            created_alias, created = book.aliases.get_or_create(scheme=scheme, value=value)
            if created:
                created_aliases.append(created_alias)
        except IntegrityError, e:
            # tried to create alias, but value clashed with another book's alias
            existing_alias = Alias.objects.get(value=value)
            errors.append('Duplicate {} found on book "{}" with value {}'.format(scheme, existing_alias.book.id, value))

    if errors:
        # here we tell the user about errors and suggest book xml files to fix
        print colored('"{}" not saved'.format(book.id), 'red')
        for error in errors:
            print colored(error, 'yellow')

        print colored("Did you mean to update or add a new edition for one of the following?", "blue")
        isbn_10_match, other_matches = Alias.get_probable_matches(aliases)
        if isbn_10_match:
            print colored("**ISBN-10 match: {}".format(isbn_10_match.id), "blue", attrs=['bold'])
        for match in other_matches:
            print colored("{} match: {}".format(match.scheme, match.book.id), "blue")

        # do not proceed with any created books or aliases if there have been errors
        if book_created:
            book.delete()
        for alias in created_aliases:
            alias.delete()
    else:
        book.save()
        print colored('"{}" {}'.format(book.id, 'saved' if book_created else 'updated'), 'green')
