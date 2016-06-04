#!/usr/bin/env python

import re
from bs4 import BeautifulSoup

#Get teams from text file
teams=[]
with open('../static/data/all_teams.txt','r') as f:
  teams = f.read().split("\n")
teams = teams[:-1]

with open('UEFA_Euro_2016.html','r') as f:
  raw_html=f.read()

main_soup = BeautifulSoup(raw_html,'html.parser')

shutout_count={}
for team in teams:
    shutout_count[team] = 0

games_finished=main_soup.find_all('a',href=re.compile('_vs_'),text=re.compile(u'[0-9]*\u2013[0-9]*'))
for game in games_finished:
    home_goals=int(game.string.split(u"\u2013")[0])
    away_goals=int(game.string.split(u"\u2013")[1])
    try:
        home_team=game.find_parent('th').find_previous_sibling('th').a.string
        away_team=game.find_parent('th').find_next_sibling('th').a.string
    except AttributeError:
        #Somebody decided to change these to td's from th's
        #They may decide to change it back...
        home_team=game.find_parent('td').find_previous_sibling('td').a.string
        away_team=game.find_parent('td').find_next_sibling('td').a.string
    if home_goals == 0:
        shutout_count[away_team] +=1
    if away_goals == 0:
        shutout_count[home_team] +=1

print "# {0} games finished".format(len(games_finished))
for team in teams:
    print "{0},{1}".format(team,shutout_count[team])

