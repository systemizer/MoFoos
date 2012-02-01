from django.db import models
from django.contrib.auth.models import *
from django.db.models import Q
from django.core.exceptions import ValidationError

from foos.stats.models import OutcomeUpdate, ScoreUpdate, Update

class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name="profile",blank=True,null=True)
    image = models.ImageField(upload_to="%m/%y/%d/",null=True,blank=True)
    bio = models.TextField(blank=True,null=True)


    def get_record(self):
        teams = Team.get_teams_by_user(self.user)
        wins = sum([team.wins.count() for team in teams])
        losses = sum([team.losses.count() for team in teams])
        return (wins,losses)

    def get_teams(self):
        return Team.get_teams_by_user(self.user)
        
class Team(models.Model):
    name = models.CharField(max_length=255,unique=True)
    bio = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to="%m/%y/%d/",null=True,blank=True)
    player1 = models.ForeignKey(User,related_name="teams_player1")
    player2 = models.ForeignKey(User,blank=True,null=True,related_name="teams_player2")
    deleted = models.BooleanField(default=False)


    def is_valid(self):
        return self.player1 and self.player2 and self.player1!=self.player2
    
    def get_brief_stats(self):
        return {'name':self.name,
                'id':self.id,
                'wins':self.wins.count(),
                'losses':self.losses.count()}

    def get_recent_history(self):
        return Outcome.get_team_history(self)[:10]
                
    def get_teammate(self,user):
        if self.player1==user:
            return self.player2
        elif self.player2==user:
            return self.player1
        else:
            return None

    def __unicode__(self):
        return self.name

    def is_player(self,user):
        return user==self.player1 or user==self.player2

    def get_games(self):
        return list(set(list(self.games_team1.all())+list(self.games_team2.all())))

    @classmethod
    def get_teams_by_user(cls,user):
        return cls.objects.filter(Q(player1=user) | Q(player2=user))

    def save(self):
        if Team.objects.filter(player1=self.player1,player2=self.player2).count() or Team.objects.filter(player1=self.player2,player2=self.player1).count():
            raise ValidationError("Those players are already on a team")
        if not self.is_valid:
            raise ValidationError("There is no 'i' in team. Find a teammate")
        return super(Team,self).save()
            
class Game(models.Model):
    is_valid = models.BooleanField(default=False)
    in_progress = models.BooleanField(default=True)
    team1 = models.ForeignKey(Team,related_name="games_team1")
    team2 = models.ForeignKey(Team,related_name="games_team2")
    team1_score = models.IntegerField(default=0)
    team2_score = models.IntegerField(default=0)
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now = True)
    score_limit = models.IntegerField(default=10)

    def __unicode__(self):
        return "%s vs %s" % (self.team1.name,self.team2.name)

    @classmethod
    def get_current_games_by_user(cls,user):
        player_teams = Team.get_teams_by_user(user)
        return cls.objects.filter(in_progress=True).filter(Q(team1__in=player_teams) | Q(team2__in=player_teams))

    @classmethod
    def get_games_by_team(cls,team):
        return cls.objects.filter(Q(team1=team) | Q(team2=team))

    def get_context_for_user(self,user):
        if not user:
            return {}
        if self.team1.is_player(user):
            return {'players_team':self.team1.name,
                    'players_score':self.team1_score,
                    'opponents_team':self.team2.name,
                    'opponents_score':self.team2_score,
                    'gid':self.id,
                    'is_valid':self.is_valid}            
        elif self.team2.is_player(user):
            return {'players_team':self.team2.name,
                    'players_score':self.team2_score,
                    'opponents_team':self.team1.name,
                    'opponents_score':self.team1_score,
                    'gid':self.id,
                    'is_valid':self.is_valid}         
        else:
            return {}

class Outcome(models.Model):
    game = models.OneToOneField(Game,related_name="outcome")
    winner = models.ForeignKey(Team,related_name="wins")
    loser = models.ForeignKey(Team,related_name="losses")
    winner_score = models.IntegerField()
    loser_score = models.IntegerField()
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s-%s vs %s-%s" % (self.winner.name,
                                   self.winner_score,
                                   self.loser.name,
                                   self.loser_score)

    def save(self):
        result = super(Outcome,self).save()
        update = Update(update_text = OutcomeUpdate.text_template % (self.winner.name,
                                                                       self.loser.name,
                                                                       self.winner_score,
                                                                       self.loser_score),
                               update_url = OutcomeUpdate.url_template % self.id,
                               created = self.created)
        update.save()
        return result

    @classmethod
    def get_team_history(cls,team):
        return Outcome.objects.filter(Q(winner=team) | Q(loser=team)).order_by('-created')

class ScoreStats(models.Model):
    scoring_team = models.ForeignKey(Team,related_name="team_scores")
    scoring_team_score = models.IntegerField()
    defender_team = models.ForeignKey(Team,related_name="team_scored_against")
    defender_team_score = models.IntegerField()
    game = models.ForeignKey(Game,related_name="score_stats")
    created = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    @classmethod
    def delete_last_stat(cls,game,team):
        if not team or not game:
            pass
        else:
            cls.objects.filter(game=game).filter(scoring_team=team).order_by("-created")[0].delete()
    
    def save(self):
        result = super(ScoreStats,self).save()
        Update(update_text = ScoreUpdate.text_template % (self.scoring_team.name,
                                                               self.defender_team.name,
                                                               self.scoring_team_score,
                                                               self.defender_team_score),
                    update_url = "",
                    created = self.created).save()
        

        return result
        

class NakedLap(models.Model):
    team = models.ForeignKey(Team,related_name="naked_laps")
    game = models.OneToOneField(Game,related_name="naked_lap")
    deleted = models.BooleanField(default=False)
    is_reversed = models.BooleanField(default=False)
