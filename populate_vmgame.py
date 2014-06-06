#!/usr/bin/env python

import os

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

    for gr in ["A","B","C","D","E","F","G","H"]:
        group_file = os.path.join(data_directory,"Group-{0}.txt".format(gr))
        with open(group_file,'r') as f:
            group_team_names = f.readline()
        group_team_names = group_team_names.split("|")

        g = Group(name="Group {0}".format(gr))
        g.save()
        for gtn in group_team_names:
           t = Team(country=gtn.strip(),group=g)
           t.save()

    #players in *-players.txt
    team_files = [tf for tf in os.listdir(data_directory) if tf.endswith('-players.txt')]
    for tf in team_files:
        country_name = tf.replace('-players.txt','')
        with open(os.path.join(data_directory,tf),'r') as f:
            player_lines = f.readlines()
        position = "Goal Keeper"
        for line in player_lines:
            if line[0] == "%":
                pretty_country_name = line[2:].strip()
            elif line[0] == "#":
                position = line[2:].strip()
            else:
                player_name = line[:].strip()
                print pretty_country_name
                t = Team.objects.get(country=pretty_country_name)
                p = Player(name=player_name,team=t,position=position)
                p.save()
       

# Start execution here!
if __name__ == '__main__':
    print "Starting VM Game population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vmgame_website.settings')
    from vmgame.models import Team,Player,Group,Scoring
    populate_players_and_teams()

    #make Scoring
    try: Scoring.objects.all().delete()
    except: pass
    scoring = Scoring(name="ORIGINAL")
    scoring.save()
