from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseBadRequest


def index(request):
    return render_to_response("index.html",{},RequestContext(request))

def new_game(request):
    score_limit = request.POST.get("score_limit") or 10
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
        return render_to_response("game.html",{},RequestContext(request))
    except ObjectDoesNotExist:
        return HttpResponseBadRequest("Failed to create game")
        

############
## AJAX GAME HANDLERS
############

#TODO: Make these ajax only

def start_game(request):
    gid = request.POST.get("gid")
    tid = request.POST.get("tid")
    if not gid or not tid:
        return HttpResponseBadRequest("Missing gid or tid")

def win_game(request):
    gid = request.POST.get("gid")
    tid = request.POST.get("tid")
    if not gid or not tid:
        return HttpResponseBadRequest("Missing gid or tid")
    try:
        team = Team.objects.get(id=tid)
        game = Game.objects.get(id=gid)
        if game.win_game(team):
            return HttpResponse("OK")
        return HttpResponseBadRequest("Invalid Team(s) for game")
    except ObjectDoesNotExist:
        return HttpResponseBadRequest("Invalid team or game")                        

def increment_score(request):
    gid = request.POST.get("gid")
    tid = request.POST.get("tid")
    if not gid or not tid:
        return HttpResponseBadRequest("Missing gid or tid")
    try:
        team = Team.objects.get(id=tid)
        game = Game.objects.get(id=gid)
        if game.increment_score(team):
            return HttpResponse("OK")
        return HttpResponseBadRequest("Invalid Operation for Game")
    except ObjectDoesNotExist:
        return HttpResponseBadRequest("Invalid Team(s) for game")
    
def decrement_score(request):
    gid = request.POST.get("gid")
    tid = request.POST.get("tid")
    if not gid or not tid:
        return HttpResponseBadRequest("Missing gid or tid")
    try:
        team = Team.objects.get(id=tid)
        game = Game.objects.get(id=gid)
        if game.decrement_score(team):
            return HttpResponse("OK")
        return HttpResponseBadRequest("Invalid Operation for Game")
    except ObjectDoesNotExist:
        return HttpResponseBadRequest("Invalid Team(s) for game")

        
