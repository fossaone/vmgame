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


furthest_round={}
is_third_place={}
is_champion={}
for team in teams:
    #Counting group stage as round 1
    furthest_round[team] = 1
    is_third_place[team] = 0
    is_champion[team] = 0


round_of_16_sect=wc_soup.find('span',class_='mw-headline',id='Round_of_16',text='Round of 16').find_parent('h3')
round_of_16_matches=round_of_16_sect.find_all_next('a',href=re.compile('_vs_'))#,text=re.compile(u'[0-9]*\u2013[0-9]*'))
for match_num in range(8):
    match=round_of_16_matches[match_num]
    #home_goals=int(match.string.split(u"\u2013")[0])
    #away_goals=int(match.string.split(u"\u2013")[1])
    try:
        home_team=match.find_parent('th').find_previous_sibling('th').a.string
        furthest_round[home_team] = 2
    except AttributeError:
        #Match hasn't happend yet so there's no team link
        pass
    try:
        away_team=match.find_parent('th').find_next_sibling('th').a.string
        furthest_round[away_team] = 2
    except AttributeError:
        #Match hasn't happend yet so there's no team link
        pass
    

quarterfinals_sect=wc_soup.find('span',class_='mw-headline',id='Quarter-finals',text='Quarter-finals').find_parent('h3')
quarterfinals_matches=quarterfinals_sect.find_all_next('a',href=re.compile('_vs_'))#,text=re.compile(u'[0-9]*\u2013[0-9]*'))
for match_num in range(4):
    match=quarterfinals_matches[match_num]
    #home_goals=int(match.string.split(u"\u2013")[0])
    #away_goals=int(match.string.split(u"\u2013")[1])
    try:
        home_team=match.find_parent('th').find_previous_sibling('th').a.string
        furthest_round[home_team] = 3
    except AttributeError:
        #Match hasn't happend yet so there's no team link
        pass
    try:
        away_team=match.find_parent('th').find_next_sibling('th').a.string
        furthest_round[away_team] = 3
    except AttributeError:
        #Match hasn't happend yet so there's no team link
        pass


semifinals_sect=wc_soup.find('span',class_='mw-headline',id='Semi-finals',text='Semi-finals').find_parent('h3')
semifinals_matches=semifinals_sect.find_all_next('a',href=re.compile('_vs_'))#,text=re.compile(u'[0-9]*\u2013[0-9]*'))
for match_num in range(2):
    match=semifinals_matches[match_num]
    #home_goals=int(match.string.split(u"\u2013")[0])
    #away_goals=int(match.string.split(u"\u2013")[1])
    try:
        home_team=match.find_parent('th').find_previous_sibling('th').a.string
        furthest_round[home_team] = 4
    except AttributeError:
        #Match hasn't happend yet so there's no team link
        pass
    try:
        away_team=match.find_parent('th').find_next_sibling('th').a.string
        furthest_round[away_team] = 4
    except AttributeError:
        #Match hasn't happend yet so there's no team link
        pass


#TODO: If match ends in tie how does wikipedia report the score
try:
    third_place_match_sect=wc_soup.find('span',class_='mw-headline',id='Third_place_match',text='Third place match').find_parent('h3')
except:
    third_place_match_sect=wc_soup.find('span',class_='mw-headline',id='Third_place_play-off',text='Third place play-off').find_parent('h3')
third_place_match=third_place_match_sect.find_all_next('a',href=re.compile('_vs_'),text=re.compile(u'[0-9]*\u2013[0-9]*'))
if len(third_place_match) > 0:
    match=third_place_match[0]
    home_goals=int(match.string.split(u"\u2013")[0])
    away_goals=int(match.string.split(u"\u2013")[1])
    home_team=match.find_parent('th').find_previous_sibling('th').a.string
    away_team=match.find_parent('th').find_next_sibling('th').a.string
    if home_goals > away_goals:
        is_third_place[home_team] = 1
    else:
        is_third_place[away_team] = 1


#TODO: If match ends in tie how does wikipedia report the score
finals_sect=wc_soup.find('span',class_='mw-headline',id='Final',text='Final').find_parent('h3')
#match_regex = re.compile(ur'',re.UNICODE)
#TODO: Fix this up
finals_match=finals_sect.find_all_next('a',href=re.compile('_vs_'),text=re.compile(u'[0-9]*\u2013[0-9]*'))
if len(finals_match) > 0:
    match=finals_match[0]
    home_goals=int(match.string.split(u"\u2013")[0])
    away_goals=int(match.string.split(u"\u2013")[1])
    home_team=match.find_parent('th').find_previous_sibling('th').a.string
    away_team=match.find_parent('th').find_next_sibling('th').a.string

    furthest_round[home_team] = 5
    furthest_round[away_team] = 5

    if home_goals > away_goals:
        is_champion[home_team] = 1
    else:
        is_champion[away_team] = 1

#print "# {0} games finished".format(len(games_finished))
for team in teams:
    print "{0},{1},{2},{3}".format(team,furthest_round[team],is_third_place[team],is_champion[team])

