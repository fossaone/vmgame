#!/usr/bin/env python

import re
from bs4 import BeautifulSoup

with open('2014_FIFA_World_Cup.html','r') as f:
  raw_html=f.read()

wc_soup = BeautifulSoup(raw_html)

goal_dls=wc_soup.find('span',class_='mw-headline',id='Goalscorers',text='Goalscorers')\
                .find_parent('h3')\
                .find_next_siblings('dl')
for goal_count in goal_dls:
    goal_count_dts=goal_count.find_all('dt')
    if (len(goal_count_dts) != 1 or 
       not re.match(r'[0-9]* goal[s]*',goal_count_dts[0].string)):
        continue
    goals_scored=int(goal_count_dts[0].string.split()[0])
    for p in goal_count.find_next_sibling('div').find('ul').find_all('li'):
        print u'{0},{1}'.format(p.find_all('a')[1].string, goals_scored)

