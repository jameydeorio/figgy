# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Edition'
        db.create_table(u'storage_edition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_modified_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['storage.Book'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True)),
            ('edition_number', self.gf('django.db.models.fields.IntegerField')(default=1, null=True, blank=True)),
        ))
        db.send_create_signal(u'storage', ['Edition'])

        # Adding field 'Alias.edition'
        db.add_column(u'storage_alias', 'edition',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['storage.Edition'], null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Edition'
        db.delete_table(u'storage_edition')

        # Deleting field 'Alias.edition'
        db.delete_column(u'storage_alias', 'edition_id')


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