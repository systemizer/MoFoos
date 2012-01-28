from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name="profile")

class Team(models.Model):
    name = models.CharField()
    player1 = models.ForeignKey(User,related_name="teams")
    player2 = models.ForeignKey(User,blank=True,null=True,related_name="teams")
    deleted = models.BooleanField(default=False)

    def is_valid(self):
        return self.player1 and self.player2 and self.player1!=self.player2

    def __unicode__(self):
        return self.name
            
class Game(models.Model):
    in_progress = models.BooleanField(default=False)
    team1 = models.ForeignKey(Team,related_name="games")
    team2 = models.ForeignKey(Team,related_name="games")
    team1_score = models.IntegerField(default=0)
    team2_score = models.IntegerField(default=0)
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now = True)
    score_limit = models.IntegerField(default=10)

    def __unicode__(self):
        return "%s vs %s" % (self.team1.name,self.team2.name)

    def start(self):
        self.in_progress = True
        self.save()

    def is_done(self):
        return hasattr(self,'outcome')

    def increment_score(self,team):
        if team==self.team1:
            self.team1_score += 1
            self.save()
            return True
        elif team==self.team2:
            self.team2_score +=1
            self.save()
            return True
        else:
            return False

    def decrement_score(self,team):
        if team==self.team1:
            self.team1_score -= 1
            self.save()
        elif team==self.team2:
            self.team2_score -=1
            self.save()
        else:
            return False
        return True

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
