#!/usr/bin/env python

import re
from bs4 import BeautifulSoup

#Get teams from main page
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


#Get squads from squad page
with open('2014_FIFA_World_Cup_squads.html','r') as f:
  raw_html=f.read()

player_soup = BeautifulSoup(raw_html)

#Hard coded positions to find players
# N.B.: brittle
positions=['GK','DF','MF','FW']

player_count=0
team_player_count={}
for team_string in teams:
    team_h3=player_soup.find('span',class_="mw-headline",text=team_string).find_parent('h3')
    pos_anchors=team_h3.find_next_sibling('table').find('table').find_all('a',text=positions)
    team_player_count[team_string] = 0
    for pos_a in pos_anchors:
        print u"{0},{1},{2}".format(pos_a.find_parent('td').find_next_sibling('td').a.string,team_string,pos_a.string)
        team_player_count[team_string] += 1
        player_count += 1

print u"# Total players : {0}".format(player_count)
for team_string in teams:
    print u"# {0} players : {1}".format(team_string,team_player_count[team_string])


