#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys

def update_vmgame_results():
    data_directory= os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "static","data")

    #Group ranks
    group_ranks={}
    with open(os.path.join(data_directory,'results','group_ranks.txt'),'r') as gr_file:
        for record in gr_file.readlines():
           record = record.strip()
           if record[0] == '#': continue
           record = record.split(',')
           country_name = record[0]
           group_rank = record[1]
           team = Team.objects.get(country=country_name)
           team.group_rank = group_rank
           team.save()

    #Goalscorers
    #Reset count to zero in case a mistake was made previously
    for player in Player.objects.filter(goals_scored__gt=0):
        player.goals_scored = 0
        player.save()
    with open(os.path.join(data_directory,'results','goalscorers.txt'),'r') as gs_file:
        for record in gs_file.readlines():
           record = record.strip()
           if record[0] == '#': continue
           record = record.split(',')
           player_name = record[0]
           goals_scored = int(record[1])
           print player_name
           #FIXME: (Stupid "(c)" for captains)
           try:
               player = Player.objects.get(name=player_name)
           except Player.DoesNotExist:
               try:
                   player = Player.objects.get(name=player_name+u" (c)")
               except Player.DoesNotExist:
                   print "WARNING: Could not find player with name "+player_name
                   continue
           player.goals_scored = goals_scored
           player.save()

    #Shutouts
    #Reset count to zero in case a mistake was made previously
    for team in Team.objects.filter(shutouts__gt=0):
        team.shutouts = 0
        team.save()
    with open(os.path.join(data_directory,'results','shutouts.txt'),'r') as so_file:
        for record in so_file.readlines():
           record = record.strip()
           if record[0] == '#': continue
           record = record.split(',')
           country_name = record[0]
           shutouts = int(record[1])
           team = Team.objects.get(country=country_name)
           team.shutouts = shutouts
           team.save()


    #TODO: Knockout stage


# Start execution here!
if __name__ == '__main__':
    print "Starting VM Game population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vmgame_website.settings')
    from vmgame.models import Team,Player,Group,Scoring
    update_vmgame_results()

