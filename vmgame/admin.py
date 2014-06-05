from django.contrib import admin
from vmgame.models import Team, Pick, UserProfile, Group, Player

# Register your models here.
admin.site.register(Team)
admin.site.register(Group)
admin.site.register(Player)
admin.site.register(Pick)
admin.site.register(UserProfile)
