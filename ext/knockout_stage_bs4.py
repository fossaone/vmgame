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


furthest_round={}
is_third_place={}
is_champion={}
for team in teams:
    #Counting group stage as round 1
    furthest_round[team] = 1
    is_third_place[team] = 0
    is_champion[team] = 0

print "# Knockout disabled until Wikipedia starts updating match pages"
round_of_16_sect=main_soup.find('span',class_='mw-headline',id='Round_of_16',text='Round of 16').find_parent('h3')
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
    

quarterfinals_sect=main_soup.find('span',class_='mw-headline',id='Quarter-finals',text='Quarter-finals').find_parent('h3')
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


semifinals_sect=main_soup.find('span',class_='mw-headline',id='Semi-finals',text='Semi-finals').find_parent('h3')
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


"""
#TODO: If match ends in tie how does wikipedia report the score
try:
    third_place_match_sect=main_soup.find('span',class_='mw-headline',id='Third_place_match',text='Third place match').find_parent('h3')
except:
    third_place_match_sect=main_soup.find('span',class_='mw-headline',id='Third_place_play-off',text='Third place play-off').find_parent('h3')
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
"""


#TODO: If match ends in tie how does wikipedia report the score
finals_sect=main_soup.find('span',class_='mw-headline',id='Final',text='Final').find_parent('h3')
#match_regex = re.compile(ur'',re.UNICODE)
#TODO: Fix this up
finals_match=finals_sect.find_all_next('a',href=re.compile('Final'),text=re.compile(u'[0-9]*\u2013[0-9]*'))
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

