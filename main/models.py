from django.db import models
from django.contrib.auth.models import *
from django.db.models import Q

class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name="profile",blank=True,null=True)

class Team(models.Model):
    name = models.CharField(max_length="63")
    player1 = models.ForeignKey(User,related_name="teams_player1")
    player2 = models.ForeignKey(User,blank=True,null=True,related_name="teams_player2")
    deleted = models.BooleanField(default=False)

    def is_valid(self):
        return self.player1 and self.player2 and self.player1!=self.player2
    
    def __unicode__(self):
        return self.name

    def is_player(self,user):
        return user==self.player1 or user==self.player2

    def get_games(self):
        return list(set(list(self.games_team1.all())+list(self.games_team2.all())))

    @classmethod
    def get_teams_by_user(cls,user):
        return cls.objects.filter(Q(player1=user) | Q(player2=user))


            
class Game(models.Model):
    in_progress = models.BooleanField(default=False)
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

    def currently_playing(self,team):
        return Game.objects.filter(in_progress=True).filter(Q(team1=team) | Q(team2=team))

    @classmethod
    def get_games_by_team(self,team):
        return Game.objects.filter(Q(team1=team) | Q(team2=team))

    def get_context_for_user(self,user):
        if not user:
            return {}
        if self.team1.is_player(user):
            return {'players_team':self.team1.name,
                    'players_score':self.team1_score,
                    'opponents_team':self.team2.name,
                    'opponents_score':self.team2_score,
                    'gid':self.id}            
        elif self.team2.is_player(user):
            return {'players_team':self.team2.name,
                    'players_score':self.team2_score,
                    'opponents_team':self.team1.name,
                    'opponents_score':self.team1_score,
                    'gid':self.id}            
        else:
            return {}

    def win_game(self,team):
        if team==self.team1 and self.team1_score==self.score_limit-1:
            self.team1_score += 1
            self.save()
            outcome = Outcome(game=self,
                              winner=self.team1,
                              loser=self.team2,
                              winner_score=self.team1_score,
                              loser_score=self.team2_score)
            outcome.save()
        elif team==self.team2 and self.team2_score==self.score_limit-1:
            self.team2_score += 1
            self.save()
            outcome = Outcome(game=self,
                              winner=self.team2,
                              loser=self.team1,
                              winner_score=self.team2_score,
                              loser_score=self.team1_score)
            outcome.save()
        else:
            return False
        return True



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

class ScoreStats(models.Model):
    #scorer = models.ForeignKey(User,related_name="scores")
    scoring_team = models.ForeignKey(Team,related_name="team_scores")
    defender_team = models.ForeignKey(Team,related_name="team_scored_against")
    #defender = models.ForeignKey(User,related_name="scored_against")
    game = models.ForeignKey(Game,related_name="score_stats")
    created = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    @classmethod
    def delete_last_stat(cls,game,team):
        if not team or not game:
            pass
        else:
            cls.objects.filter(game=game).filter(scoring_team=team).order_by("-created")[0].delete()
    
class NakedLap(models.Model):
    team = models.ForeignKey(Team,related_name="naked_laps")
    game = models.OneToOneField(Game,related_name="naked_lap")
    deleted = models.BooleanField(default=False)
    is_reversed = models.BooleanField(default=False)
