from foos.main.models import Game
from django.forms import ModelForm
from foos.main.models import Team


class EditTeamForm(ModelForm):
    class Meta:
        model = Team
        exclude = ('player1','player2','deleted')
