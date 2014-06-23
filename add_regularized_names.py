#!/usr/bin/env python

import os
from unidecode import unidecode

def add_regularized_names():
    for p in Player.objects.all():
        p.name_regularized = unidecode(p.name).lower()
        p.save()

    for t in Team.objects.all():
        t.country_regularized = unidecode(t.country).lower()
        t.save()

# Start execution here!
if __name__ == '__main__':
    print "Starting VM Game population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vmgame_website.settings')
    from vmgame.models import Team,Player
    add_regularized_names()

