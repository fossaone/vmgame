#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys
import codecs
from unidecode import unidecode

def update_vmgame_results():
    data_directory= os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "static","data")

    #Group ranks
    group_ranks={}
    with codecs.open(os.path.join(data_directory,'results','group_ranks.txt'),'r',encoding='utf-8') as gr_file:
        for record in gr_file.readlines():
           record = record.strip()
           if record[0] == '#': continue
           record = record.split(u',')
           country_name_regularized = unidecode(record[0]).lower()
           group_rank = record[1]
           team = Team.objects.get(country_regularized=country_name_regularized)
           team.group_rank = group_rank
           team.save()

    #Goalscorers
    #Reset count to zero in case a mistake was made previously
    for player in Player.objects.filter(goals_scored__gt=0):
        player.goals_scored = 0
        player.save()
    with codecs.open(os.path.join(data_directory,'results','goalscorers.txt'),'r',encoding='utf-8') as gs_file:
        for record in gs_file.readlines():
           record = record.strip()
           if record[0] == '#': continue
           record = record.split(u',')
           player_name_regularized = unidecode(record[0]).lower()
           goals_scored = int(record[1])
           #print player_name_regularized
           #FIXME: (Stupid "(c)" for captains)
           try:
               player = Player.objects.get(name_regularized=player_name_regularized)
           except Player.DoesNotExist:
               try:
                   player = Player.objects.get(name_regularized=player_name_regularized+u' (c)')
               except Player.DoesNotExist:
                   try:
                       player_name_regularized_list = player_name_regularized.split(u' ')
                       player_first_name = player_name_regularized_list[0]
                       player_last_name = player_name_regularized_list[-1]
                       player = Player.objects.filter(name_regularized__contains=player_last_name).get(name_regularized__contains=player_first_name)
                       print "WARNING: Did not find exact match for player with regularized name "+player_name_regularized
                       print "         Using inexact match with regularized name "+player.name_regularized
                   except Player.DoesNotExist:
                       print "WARNING: Could not find player with regularized name "+player_name_regularized \
                             + " ({0} goal(s))".format(goals_scored)
                       continue
           player.goals_scored = goals_scored
           player.save()

    #Shutouts
    #Reset count to zero in case a mistake was made previously
    for team in Team.objects.filter(shutouts__gt=0):
        team.shutouts = 0
        team.save()
    with codecs.open(os.path.join(data_directory,'results','shutouts.txt'),'r',encoding='utf-8') as so_file:
        for record in so_file.readlines():
           record = record.strip()
           if record[0] == '#': continue
           record = record.split(u',')
           country_name_regularized = unidecode(record[0]).lower()
           shutouts = int(record[1])
           team = Team.objects.get(country_regularized=country_name_regularized)
           team.shutouts = shutouts
           team.save()


    #TODO: Knockout stage


# Start execution here!
if __name__ == '__main__':
    print "Starting VM Game population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vmgame_website.settings')
    from vmgame.models import Team,Player,Group,Scoring,update_scores
    update_vmgame_results()
    update_scores()

