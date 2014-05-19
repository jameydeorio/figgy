# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName". 
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.
        for book in orm.Book.objects.all():
            # create an edition for each book and move all aliases to edition
            edition = orm.Edition(title=book.title, description=book.description)
            edition.book = book
            edition.save()
            aliases = book.aliases.all()
            for alias in aliases:
                scheme = alias.scheme
                value = alias.value
                alias.delete()
                alias = orm.Alias.objects.create(scheme=scheme, value=value, edition=edition, book=book)
                alias.save()
            edition.save()
            book.save()


    def backwards(self, orm):
        "Write your backwards methods here."
        raise RuntimeError("Cannot reverse this migration.")

    models = {
        u'storage.alias': {
            'Meta': {'object_name': 'Alias'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'aliases'", 'to': u"orm['storage.Book']"}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'edition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['storage.Edition']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'scheme': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'value': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        u'storage.book': {
            'Meta': {'ordering': "['title']", 'object_name': 'Book'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '30', 'primary_key': 'True'}),
            'last_modified_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'})
        },
        u'storage.edition': {
            'Meta': {'object_name': 'Edition'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['storage.Book']"}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'edition_number': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'})
        }
    }

    complete_apps = ['storage']
    symmetrical = True
