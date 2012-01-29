import json

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import Http404, HttpResponseBadRequest, HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login as auth_login
from django.conf import settings

from foos.main.models import *
from foos.main.decorators import ajax_required

def index(request):
    if request.user.is_authenticated():
        player_teams = Team.get_teams_by_user(request.user)        
        players = User.objects.exclude(id=request.user.id)
    else:
        player_teams = []
        players = []
        
    opponent_teams = [t for t in Team.objects.all() if t not in player_teams]

    register_form = UserCreationForm()
    login_form = AuthenticationForm()

    return render_to_response("index.html",
                              {'player_teams':player_teams,                               
                               'opponent_teams':opponent_teams,
                               'players':players,
                               'register_form':register_form,
                               'login_form':login_form},
                              RequestContext(request))

def new_game(request):
    if request.method=="POST":
        score_limit = 10 #hardcoded for now
        tid = request.POST.get("tid")
        against = request.POST.get("against") or None
        try:
            team = Team.objects.get(id=tid)
            if against:
                team_against = Team.objects.get(id=against)
            else:
                team_against = None
            game = Game(team1=team,
                        team2=team_against,
                        score_limit=score_limit)
            game.save()
            game_context = game.get_context_for_user(request.user)
            return HttpResponse(json.dumps(game_context))
        except ObjectDoesNotExist:
            return HttpResponseBadRequest("Failed to create game")
    else:
        raise Http404

                        

def play_game(request):
    gid = request.GET.get("gid")
    context = {}
    if not gid:
        return HttpResponseBadRequest("Could not determine game id")
    try:
        game = Game.objects.select_related(depth=1).get(id=gid)
        game_context = game.get_context_for_user(request.user)
        return render_to_response("game.html",game_context,RequestContext(request))        
    except ObjectDoesNotExist:
        return HttpResponseBadRequest("Invalid Game ID")

############
## AJAX GAME HANDLERS
############

#TODO: Make these ajax only

def make_team(request):
    if request.method=="POST":
        team_name = request.POST.get("team_name")
        uid = request.POST.get("uid")
        if not uid or not team_name:
            return HttpResponseBadRequest("Bad uid or team name")
        try:
            player = User.objects.get(id=uid)
            team = Team(name=team_name,
                        player1 = request.user,
                        player2 = player)
            team.save()
            return HttpResponse("OK")
        except ObjectDoesNotExist:
            return HttpResponseBadRequest("User does not exist")
        except ValidationError:
            return HttpResponseBadRequest("Could not create team. Team might already exist")
    else:
        raise Http404


def increment_score(request):
    gid = request.GET.get("gid")
    if not gid:
        return HttpResponseBadRequest("Missing gid")
    try:        
        game = Game.objects.get(id=gid)
        user_teams = Team.get_teams_by_user(request.user)

        if game.team1 in user_teams:
            game.team1_score += 1                
            game.save()
            ScoreStats(scoring_team=game.team1,
                      defender_team = game.team2,
                      game = game).save()



        elif game.team2 in user_teams:
            game.team2_score +=1
            game.save()
            ScoreStats(scoring_team=game.team2,
                      defender_team = game.team1,
                      game = game).save()


        else:
            return HttpResponseBadRequest("User is not currently playing")

        #check if the game is over
        if game.team1_score==game.score_limit:
            outcome = Outcome(game=game,
                              winner=game.team1,
                              loser=game.team2,
                              winner_score=game.team1_score,
                              loser_score=game.team2_score)
            outcome.save()
            game.in_progress = False
            game.save()
        elif game.team2_score==game.score_limit:
            outcome = Outcome(game=game,
                              winner=game.team2,
                              loser=game.team1,
                              winner_score=game.team2_score,
                              loser_score=game.team1_score)
            outcome.save()
            game.in_progress = False
            game.save()            

        return HttpResponse(json.dumps(game.get_context_for_user(request.user)))

    except ObjectDoesNotExist:
        return HttpResponseBadRequest("Invalid Team(s) for game")

def decrement_score(request):
    gid = request.GET.get("gid")
    if not gid:
        return HttpResponseBadRequest("Missing gid")
    try:        
        game = Game.objects.get(id=gid)
        user_teams = Team.get_teams_by_user(request.user)
        if game.team1 in user_teams:
            game.team1_score -= 1
            game.save()
            ScoreStats.delete_last_stat(game,game.team1)

        elif game.team2 in user_teams:
            game.team2_score -= 1
            game.save()
            ScoreStats.delete_last_stat(game,game.team1)
        else:
            return HttpResponseBadRequest("User is not currently playing")

        return HttpResponse(json.dumps(game.get_context_for_user(request.user)))

    except ObjectDoesNotExist:
        return HttpResponseBadRequest("Invalid Team(s) for game")

def refresh_score(request):
    gid = request.GET.get("gid")
    if not gid:
        return HttpResponseBadRequest("Missing gid")
    try:        
        game = Game.objects.get(id=gid)
        return HttpResponse(json.dumps(game.get_context_for_user(request.user)))
    except ObjectDoesNotExist:
        return HttpResponseBadRequest("Invalid game")

def register(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        user = form.save()
        user = authenticate(username=user.username,password=request.POST.get("password1"))
        profile = UserProfile(user=user)
        profile.save()
        auth_login(request,user)
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
        return HttpResponseRedirect("/")
    else:
        return HttpResponseBadRequest("Invalid username or password")
        
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Okay, security checks complete. Log the user in.
            auth_login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return HttpResponse("OK")
        else:
            return HttpResponseBadRequest("Invalid username or password")
    else:
        raise Http404
