import json

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import Http404, HttpResponseBadRequest, HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate,login as auth_login
from django.conf import settings

from foos.main.models import *
from foos.main.decorators import ajax_required, login_required

def index(request):
    if request.user.is_authenticated():
        player_teams = Team.get_teams_by_user(request.user)        
        player_teams_context = [(t.name,t.get_teammate(request.user),t.id) for t in player_teams]
        players = User.objects.exclude(id=request.user.id)
        current_games = Game.get_current_games_by_user(request.user)
    else:
        player_teams = []
        player_teams_context = []
        players = []
        current_games = []
        
    opponent_teams = [t for t in Team.objects.all() if t not in player_teams]
    opponent_teams_context = [(t.name,t.player1,t.player2,t.id) for t in opponent_teams]

    register_form = UserCreationForm()
    login_form = AuthenticationForm()

    return render_to_response("index.html",
                              {'player_teams':player_teams_context,         
                               'current_games':current_games,
                               'opponent_teams':opponent_teams_context,
                               'players':players,
                               'register_form':register_form,
                               'login_form':login_form},
                              RequestContext(request))


############
## AJAX GAME HANDLERS
############


@login_required
@ajax_required
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

            #check if a duplicate game exists
            possible_dups = Game.objects.filter(is_valid=False,
                                   in_progress=True,
                                   team1_score=0,
                                   team2_score=0)
            if possible_dups.filter(team1=team,team2=team_against).exists():
                game = possible_dups.filter(team1=team,team2=team_against)[0]
            elif possible_dups.filter(team1=team_against,team2=team).exists():
                game = possible_dups.filter(team1=team_against,team2=team)[0]
            else:
                                   
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

@login_required
@ajax_required
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

@login_required
@ajax_required
def increment_score(request):
    gid = request.GET.get("gid")
    if not gid:
        return HttpResponseBadRequest("Missing gid")
    try:        
        game = Game.objects.get(id=gid)
        if not game.is_valid:
            return HttpResponseBadRequest("Game needs to be validated by opposing team. Please wait.")
        user_teams = Team.get_teams_by_user(request.user)

        if game.team1 in user_teams:

            if game.team1_score==0:
                game.naked_lap_in_effect = game.team2
            elif game.naked_lap_in_effect==game.team1:
                game.naked_lap_in_effect = None

            game.team1_score += 1                
            game.save()
            ScoreStats(scoring_team=game.team1,
                       scoring_team_score = game.team1_score,
                      defender_team = game.team2,
                       defender_team_score = game.team2_score,
                      game = game).save()



        elif game.team2 in user_teams:

            if game.team2_score==0:
                game.naked_lap_in_effect = game.team1
            elif game.naked_lap_in_effect==game.team2:
                game.naked_lap_in_effect = None

            game.team2_score +=1
            game.save()
            ScoreStats(scoring_team=game.team2,
                       scoring_team_score = game.team2_score,
                      defender_team = game.team1,
                       defender_team_score = game.team1_score,
                      game = game).save()


        else:
            return HttpResponseBadRequest("User is not currently playing")

        #check if the game is over
        outcome = None 

        if game.team1_score>=game.score_limit:
            outcome = Outcome(game=game,
                              winner=game.team1,
                              loser=game.team2,
                              winner_score=game.team1_score,
                              loser_score=game.team2_score)
            outcome.save()
            game.in_progress = False
            game.save()

        elif game.team2_score>=game.score_limit:
            outcome = Outcome(game=game,
                              winner=game.team2,
                              loser=game.team1,
                              winner_score=game.team2_score,
                              loser_score=game.team1_score)
            outcome.save()
            game.in_progress = False
            game.is_done = True
            game.save()

        if outcome:
            outcome.update_rating()


        #check for naked lap
        if game.team2_score>=game.score_limit or game.team1_score>=game.score_limit:
            if game.naked_lap_in_effect:
                nakedlap = NakedLap(team=game.naked_lap_in_effect,
                                    game=game,
                                    is_reversed = True if game.team1_score and game.team2_score else False )
                nakedlap.save()

        return HttpResponse(json.dumps(game.get_context_for_user(request.user)))

    except ObjectDoesNotExist:
        return HttpResponseBadRequest("Invalid Team(s) for game")

@login_required
@ajax_required
def decrement_score(request):
    gid = request.GET.get("gid")
    if not gid:
        return HttpResponseBadRequest("Missing gid")
    try:        
        game = Game.objects.get(id=gid)
        if not game.is_valid:
            return HttpResponseBadRequest("Game needs to be validated by opposing team. Please wait.")
        user_teams = Team.get_teams_by_user(request.user)
        if game.team1 in user_teams:
            if game.team1_score>0:
                game.team1_score -= 1
                game.save()
                ScoreStats.delete_last_stat(game,game.team1)
        elif game.team2 in user_teams:
            if game.team2_score>0:
                game.team2_score -= 1
                game.save()
                ScoreStats.delete_last_stat(game,game.team2)
        else:
            return HttpResponseBadRequest("User is not currently playing")

        return HttpResponse(json.dumps(game.get_context_for_user(request.user)))

    except ObjectDoesNotExist:
        return HttpResponseBadRequest("Invalid Team(s) for game")

@ajax_required
def refresh_score(request):
    gid = request.GET.get("gid")
    if not gid:
        return HttpResponseBadRequest("Missing gid")
    try:        
        game = Game.objects.get(id=gid)
        players_score=  request.GET.get("players_score")
        if players_score>=0 and game.is_valid:
            user_teams = Team.get_teams_by_user(request.user)
            if game.team1 in user_teams:
                if game.team1_score>0:
                    game.team1_score = players_score
                    game.save()
                elif game.team2 in user_teams:
                    game.team2_score = players_score
                    game.save()


        #see if other team has opened game
        if not game.is_valid:
            if game.team2.is_player(request.user):
                game.is_valid = True
                game.in_progress=True
                game.save()

        return HttpResponse(json.dumps(game.get_context_for_user(request.user)))
    except ObjectDoesNotExist:
        return HttpResponseBadRequest("Invalid game")

@ajax_required
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
        
@ajax_required
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            return HttpResponse("OK")
        else:
            return HttpResponseBadRequest("Invalid username or password")
    else:
        raise Http404


#This occurs only when the user deletes a currently playing game
@login_required
@ajax_required
def end_game(request):
    gid = request.GET.get("gid")
    if gid:
        try:
            game = Game.objects.get(id=gid)
            if game.is_done():
                #dont delete the game
                pass
            else:
                game.in_progress = False
                game.deleted = True
                game.save()
            return HttpResponse("OK")
        except ObjectDoesNotExist:
            return HttpResponseBadRequest("Could not find game")
    else:
        return HttpResponseBadRequest("Could not determine game")
    
