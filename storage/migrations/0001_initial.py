# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Book'
        db.create_table(u'storage_book', (
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_modified_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=30, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal(u'storage', ['Book'])

        # Adding model 'Alias'
        db.create_table(u'storage_alias', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_modified_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(related_name='aliases', to=orm['storage.Book'])),
            ('value', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, db_index=True)),
            ('scheme', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal(u'storage', ['Alias'])


    def backwards(self, orm):
        # Deleting model 'Book'
        db.delete_table(u'storage_book')

        # Deleting model 'Alias'
        db.delete_table(u'storage_alias')


    models = {
        u'storage.alias': {
            'Meta': {'object_name': 'Alias'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'aliases'", 'to': u"orm['storage.Book']"}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
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
        }
    }

    complete_apps = ['storage']