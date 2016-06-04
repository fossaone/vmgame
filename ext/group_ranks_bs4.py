#!/usr/bin/env python

import re
from bs4 import BeautifulSoup

with open('UEFA_Euro_2016.html','r') as f:
  raw_html=f.read()

main_soup = BeautifulSoup(raw_html,'html.parser')

#Get teams from text file
teams=[]
with open('../static/data/all_teams.txt','r') as f:
  teams = f.read().split("\n")
teams = teams[:-1]

groups = main_soup.find_all('span',class_='mw-headline',id=re.compile(r'^Group_.$'))
for group in groups:
    print "#{0}".format(group.string)
    team_list = group.find_parent('h3').find_next_sibling('table').find_all('a',text=teams)
    for i,team in enumerate(team_list):
        print u"{0},{1}".format(team.string,i+1)

