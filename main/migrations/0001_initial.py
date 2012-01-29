# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'UserProfile'
        db.create_table('main_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='profile', unique=True, null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('main', ['UserProfile'])

        # Adding model 'Team'
        db.create_table('main_team', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length='63')),
            ('player1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='teams_player1', to=orm['auth.User'])),
            ('player2', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='teams_player2', null=True, to=orm['auth.User'])),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('main', ['Team'])

        # Adding model 'Game'
        db.create_table('main_game', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('in_progress', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('team1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='games_team1', to=orm['main.Team'])),
            ('team2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='games_team2', to=orm['main.Team'])),
            ('team1_score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('team2_score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('score_limit', self.gf('django.db.models.fields.IntegerField')(default=10)),
        ))
        db.send_create_signal('main', ['Game'])

        # Adding model 'Outcome'
        db.create_table('main_outcome', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.OneToOneField')(related_name='outcome', unique=True, to=orm['main.Game'])),
            ('winner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='wins', to=orm['main.Team'])),
            ('loser', self.gf('django.db.models.fields.related.ForeignKey')(related_name='losses', to=orm['main.Team'])),
            ('winner_score', self.gf('django.db.models.fields.IntegerField')()),
            ('loser_score', self.gf('django.db.models.fields.IntegerField')()),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('main', ['Outcome'])


    def backwards(self, orm):
        
        # Deleting model 'UserProfile'
        db.delete_table('main_userprofile')

        # Deleting model 'Team'
        db.delete_table('main_team')

        # Deleting model 'Game'
        db.delete_table('main_game')

        # Deleting model 'Outcome'
        db.delete_table('main_outcome')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.game': {
            'Meta': {'object_name': 'Game'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_progress': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'score_limit': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'team1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'games_team1'", 'to': "orm['main.Team']"}),
            'team1_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'team2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'games_team2'", 'to': "orm['main.Team']"}),
            'team2_score': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'main.outcome': {
            'Meta': {'object_name': 'Outcome'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'game': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'outcome'", 'unique': 'True', 'to': "orm['main.Game']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loser': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'losses'", 'to': "orm['main.Team']"}),
            'loser_score': ('django.db.models.fields.IntegerField', [], {}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wins'", 'to': "orm['main.Team']"}),
            'winner_score': ('django.db.models.fields.IntegerField', [], {})
        },
        'main.team': {
            'Meta': {'object_name': 'Team'},
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': "'63'"}),
            'player1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'teams_player1'", 'to': "orm['auth.User']"}),
            'player2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'teams_player2'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'main.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'profile'", 'unique': 'True', 'null': 'True', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['main']
