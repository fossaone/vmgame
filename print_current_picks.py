#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

# Start execution here!
if __name__ == '__main__':
    import django
    os.environ['DJANGO_SETTINGS_MODULE'] = 'vmgame_website.settings'
    django.setup()
    from vmgame.models import Team,Player,Group,Scoring,Event,print_all_picks
    print_all_picks()

