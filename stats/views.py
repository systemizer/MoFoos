from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseBadRequest
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from django.contrib.auth.forms import AuthenticationForm

from foos.main.decorators import login_required
from foos.stats.forms import UserProfileForm
from foos.stats.models import *
from foos.main.models import Outcome, Team


def index(request):
    updates = Update.objects.all().order_by("-created")[:20]
    teams = Team.objects.all()
    teams = sorted(teams,key=lambda k: -(k.wins.count()*1.5 - k.losses.count()))
    login_form = AuthenticationForm()
    return render_to_response("stats_index.html",{'updates':updates,
                                                  'teams' : teams,
                                                  'login_form':login_form},
                              RequestContext(request))
                              

def view_outcome(request):
    oid = request.GET.get("oid")
    if not oid:
        raise Http404
    try:
        outcome = Outcome.objects.get(id=oid)
        return render_to_response("view_outcome.html",{'outcome':outcome},RequestContext(request))
    except ObjectDoesNotExist:
        return HttpResponseBadRequest("Outcome with oid %s does not exist" % oid)



def profile(request):
    uid = request.GET.get("uid")
    if not uid:
        raise Http404
    try:
        user = User.objects.get(id=uid)
        profile = user.get_profile()
        if request.method=="GET":
            if user == request.user:
                form = UserProfileForm(instance=profile)
                return render_to_response("edit_profile.html",{'form':form,
                                                               'profile':profile},RequestContext(request))
            else:
                return render_to_response("profile.html",{'profile':profile},RequestContext(request))
        elif request.method=="POST":
            if user != request.user:
                return HttpResponseForbidden()
            form = UserProfileForm(request.POST,request.FILES,instance=profile)
            if form.is_valid():
                form.save()
            return render_to_response("edit_profile.html",{'form':form,
                                                           'profile':profile},
                                      RequestContext(request))
        else:
            raise Http404
    except ObjectDoesNotExist:
        return HttpResponseBadRequest("User does not exist")
        

                
def view_team(request):
    tid = request.GET.get("tid")
    if not tid:
        return HttpResponseBadRequest("Could not find team")
    else:
        try: 
            team = Team.objects.get(id=tid)
            if team.is_player(request.user):
                edit= True
            else:
                edit = False
            
            return render_to_response("view_team.html",{'team':team,'edit':edit},RequestContext(request))
        except ObjectDoesNotExist:
            return HttpResponseBadRequest("Could not find team")


@login_required
def edit_team(request):
    tid = request.GET.get("tid")
    if not tid:
        return HttpResponseBadRequest("Could not find team")
    try:
        team = Team.objects.get(id=tid)
        if not team.is_player(request.user):
            return HttpResponseBadRequest("You cannot edit a team that you are not on")
        if request.method=="GET":
            form = EditTeamForm(instance=team)
            return render_to_response("edit_team.html",{'form':form},RequestContext(request))
        elif request.method=="POST":
            form = EditTeamForm(request.POST,request.FILES,instance=team)
            if form.is_valid():
                form.save()
            return render_to_response("edit_team.html",{'form':form},RequestContext(request))
        else:
            raise Http404
    except ObjectDoesNotExist:
        return HttpResponseBadRequest("Could not find team")

            
