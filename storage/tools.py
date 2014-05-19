# encoding: utf-8
# Created by David Rideout <drideout@safaribooksonline.com> on 2/7/14 4:58 PM
# Copyright (c) 2013 Safari Books Online, LLC. All rights reserved.
from django.db import IntegrityError
from termcolor import colored

from storage.models import Book, Edition


def process_book_element(book_element):
    """
    Process a book element into the database.

    :param book: book element
    :returns:
    """
    book_id = book_element.get('id')
    aliases = [alias for alias in book_element.xpath('aliases/alias')]
    isbn_13 = [alias.get('value') for alias in aliases if alias.get('scheme') == 'ISBN-13'][0]
    edition, edition_created, book_created = Edition.objects.get_or_create_by_isbn_13(isbn_13, book_id)

    book = edition.book
    title = book_element.findtext('title')
    description = book_element.findtext('description')
    book.title = edition.title = title
    book.description = edition.description = description
    if edition_created:
        # subtract one because we just made this edition, and it will default to 1
        edition.edition_number = book_element.findtext('edition') or edition.book.get_next_edition_number()
    else:
        edition.edition_number = book_element.findtext('edition') or edition.edition_number

    for alias in aliases:
        scheme = alias.get('scheme')
        value = alias.get('value')

        try:
            edition.aliases.get_or_create(scheme=scheme, value=value)
        except IntegrityError:
            if book_created:
                book.delete()
            if edition_created:
                edition.delete()
            return colored("{} not saved".format(edition), "red")

    book.save()
    edition.save()
    return colored("{} {}".format(edition, "saved" if edition_created else "updated"), "green")
