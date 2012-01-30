# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Update'
        db.create_table('stats_update', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('update_text', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('update_url', self.gf('django.db.models.fields.CharField')(max_length=127)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('stats', ['Update'])

        # Adding model 'OutcomeUpdate'
        db.create_table('stats_outcomeupdate', (
            ('update_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['stats.Update'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('stats', ['OutcomeUpdate'])


    def backwards(self, orm):
        
        # Deleting model 'Update'
        db.delete_table('stats_update')

        # Deleting model 'OutcomeUpdate'
        db.delete_table('stats_outcomeupdate')


    models = {
        'stats.outcomeupdate': {
            'Meta': {'object_name': 'OutcomeUpdate', '_ormbases': ['stats.Update']},
            'update_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['stats.Update']", 'unique': 'True', 'primary_key': 'True'})
        },
        'stats.update': {
            'Meta': {'object_name': 'Update'},
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'update_text': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'update_url': ('django.db.models.fields.CharField', [], {'max_length': '127'})
        }
    }

    complete_apps = ['stats']
