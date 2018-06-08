#!/usr/bin/env python

import os
import sys

from unidecode import unidecode

import django
#from django.conf import settings
#settings.configure(DEBUG=True)
os.environ['DJANGO_SETTINGS_MODULE'] = 'vmgame_website.settings'
django.setup()

def populate_players_and_teams():
    #TODO: Make sure data is correct:
    data_directory= os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "static","data")

    #Clear teams and players and groups
    try:  #Throws an error if none exist
        Team.objects.all().delete()
    except: pass
    try:  #Throws an error if none exist
        Player.objects.all().delete()
    except: pass
    try:  #Throws an error if none exist
        Group.objects.all().delete()
    except: pass

    for gr in ["A","B","C","D","E","F", "G", "H"]:
        group_file = os.path.join(data_directory,"Group-{0}.txt".format(gr))
        with open(group_file,'r') as f:
            group_team_names = f.readline()
        group_team_names = group_team_names.strip("\n").split("|")

        g = Group(name="Group {0}".format(gr))
        g.save()
        for gtn in group_team_names:
           country = gtn.strip()
           country_regularized = unidecode(country).lower()
           t = Team(country=country,country_regularized=country_regularized,group=g)
           t.save()

    position_dict = { 'FW': 'Forwards',
                      'MF': 'Midfielders',
                      'DF': 'Defenders',
                      'GK': 'Goal Keepers' }
    #players in *-players.txt
    team_files = [tf for tf in os.listdir(data_directory) if tf.endswith('-players.txt')]
    for tf in team_files:
        country_name = tf.replace('-players.txt','')
        with open(os.path.join(data_directory,tf),'r',encoding="utf-8") as f:
            player_lines = f.readlines()
        for line in player_lines:
            if line.startswith("#"):
                continue
            player_name,country_name_file,position_abbr = line[:].rstrip("\n").split(",")
            name_regularized = unidecode(player_name).lower()
            position = position_dict[position_abbr]
            t = Team.objects.get(country=country_name)
            p = Player(name=player_name,name_regularized=name_regularized,team=t,position=position)
            p.save()
       

# Start execution here!
if __name__ == '__main__':
    print("Starting VM Game population script...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vmgame_website.settings')
    from vmgame.models import Team,Player,Group,Scoring
    populate_players_and_teams()

    #make Scoring
    try: Scoring.objects.all().delete()
    except: pass
    scoring = Scoring(name="ORIGINAL")
    scoring.save()
