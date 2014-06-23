#!/usr/bin/env python

import re
from bs4 import BeautifulSoup

with open('2014_FIFA_World_Cup.html','r') as f:
  raw_html=f.read()

wc_soup = BeautifulSoup(raw_html)

teams=[]
qual_sect=wc_soup.find('span',class_='mw-headline',text='Qualification').find_parent('h3')
qual_region_dls=qual_sect.find_next_sibling('table').find_all('dl')
for region_dl in qual_region_dls:
    num_quals = int(re.sub(r'^.*\(([0-9]*)\).*$',r'\1',str(region_dl.find('dt'))))
    if(num_quals==0): continue
    for team_li in region_dl.find_next_sibling('ul').find_all('li'):
        teams.append(team_li.a.string)


shutout_count={}
for team in teams:
    shutout_count[team] = 0



games_finished=wc_soup.find_all('a',href=re.compile('_vs_'),text=re.compile(u'[0-9]*\u2013[0-9]*'))
for game in games_finished:
    home_goals=int(game.string.split(u"\u2013")[0])
    away_goals=int(game.string.split(u"\u2013")[1])
    home_team=game.find_parent('th').find_previous_sibling('th').a.string
    away_team=game.find_parent('th').find_next_sibling('th').a.string
    if home_goals == 0:
        shutout_count[away_team] +=1
    if away_goals == 0:
        shutout_count[home_team] +=1

print "# {0} games finished".format(len(games_finished))
for team in teams:
    print "{0},{1}".format(team,shutout_count[team])

