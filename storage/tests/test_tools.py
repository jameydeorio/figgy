# encoding: utf-8
# Created by David Rideout <drideout@safaribooksonline.com> on 2/7/14 5:01 PM
# Copyright (c) 2013 Safari Books Online, LLC. All rights reserved.
from django.db import IntegrityError

from django.test import TestCase
from lxml import etree
from storage.models import Book, Alias, Edition
import storage.tools


class TestTools(TestCase):
    def setUp(self):
        pass
        self.valid_book_xml_str = '''
        <book id="12345">
            <title>A title</title>
            <aliases>
                <alias scheme="ISBN-10" value="0158757819"/>
                <alias scheme="ISBN-13" value="0000000000123"/>
            </aliases>
        </book>
        '''

        self.edition_2_xml_str = '''
        <book id="12345">
            <title>A title, Ed. 2</title>
            <aliases>
                <alias scheme="ISBN-10" value="0158757829"/>
                <alias scheme="ISBN-13" value="0000000000456"/>
            </aliases>
        </book>
        '''

        self.edition_2_new_title_xml_str = '''
        <book id="12345">
            <title>A different title, Ed. 2</title>
            <aliases>
                <alias scheme="ISBN-10" value="0158757829"/>
                <alias scheme="ISBN-13" value="0000000000456"/>
            </aliases>
        </book>
        '''

        self.dupe_alias_book_xml_str = '''
        <book id="54321">
            <title>Another title</title>
            <aliases>
                <alias scheme="ISBN-10" value="2222222222"/>
                <alias scheme="ISBN-13" value="0000000000123"/>
            </aliases>
        </book>
        '''

    def test_storage_tools_process_book_element_db(self):
        '''process_book_element should put the book in the database.'''

        xml = etree.fromstring(self.valid_book_xml_str)
        storage.tools.process_book_element(xml)

        self.assertEqual(Book.objects.count(), 1)
        book = Book.objects.get(pk='12345')

        self.assertEqual(book.title, 'A title')
        self.assertEqual(book.editions.all()[0].aliases.count(), 2)
        self.assertEqual(Alias.objects.get(scheme='ISBN-10').value, '0158757819')
        self.assertEqual(Alias.objects.get(scheme='ISBN-13').value, '0000000000123')

    def test_duplicate_aliases_are_not_accepted(self):
        """
        Ensure books with duplicate aliases throw an exception
        """
        xml = etree.fromstring(self.valid_book_xml_str)
        storage.tools.process_book_element(xml)
        xml = etree.fromstring(self.dupe_alias_book_xml_str)
        storage.tools.process_book_element(xml)
        self.assertEqual(1, Book.objects.count())  # invalid book was removed

    def test_new_editions_are_saved(self):
        """
        Ensure books with duplicate aliases throw an exception
        """
        xml = etree.fromstring(self.valid_book_xml_str)
        storage.tools.process_book_element(xml)
        xml = etree.fromstring(self.edition_2_xml_str)
        storage.tools.process_book_element(xml)
        self.assertEqual(1, Book.objects.count())
        self.assertEqual(2, Edition.objects.count())

    def test_editions_can_be_updated(self):
        xml = etree.fromstring(self.edition_2_xml_str)
        storage.tools.process_book_element(xml)
        xml = etree.fromstring(self.edition_2_new_title_xml_str)
        storage.tools.process_book_element(xml)
        self.assertEqual(1, Book.objects.count())
        self.assertEqual(1, Edition.objects.count())
