from django.contrib import admin
from foos.main.models import *

admin.site.register(UserProfile)
admin.site.register(Team)
admin.site.register(Game)
admin.site.register(Outcome)
admin.site.register(NakedLap)
