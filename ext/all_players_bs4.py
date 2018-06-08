#!/usr/bin/env python

import re
from bs4 import BeautifulSoup

#Get teams from text file
teams=[]
with open('../static/data/all_teams.txt','r') as f:
  teams = f.read().split("\n")
teams = teams[:-1]

#Get squads from squad page
with open('2018_FIFA_World_Cup_squads.html','r') as f:
  raw_html=f.read()

player_soup = BeautifulSoup(raw_html,'html.parser')

#Hard coded positions to find players
# N.B.: brittle
positions=['GK','DF','MF','FW']

player_count=0
team_player_count={}
for team_string in teams:
    team_h3=player_soup.find('span',class_="mw-headline",text=team_string).find_parent('h3')
    pos_anchors=team_h3.find_next_sibling('table').find_all('a',text=positions)
    team_player_count[team_string] = 0
    for pos_a in pos_anchors:
        print(u"{0},{1},{2}".format(pos_a.find_parent('td').find_next_sibling('th').a.string,team_string,pos_a.string))
        team_player_count[team_string] += 1
        player_count += 1

print(u"# Total players : {0}".format(player_count))
for team_string in teams:
    print(u"# {0} players : {1}".format(team_string,team_player_count[team_string]))


