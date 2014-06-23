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


groups = wc_soup.find_all('span',class_='mw-headline',id=re.compile(r'^Group_.$'))
for group in groups:
    print "#{0}".format(group.string)
    team_list = group.find_parent('h3').find_next_sibling('table').find_all('a',text=teams)
    for i,team in enumerate(team_list):
        print u"{0},{1}".format(team.string,i+1)

