#!/bin/bash

#NOTE: Not updating players anymore

wget -q en.wikipedia.org/wiki/2014_FIFA_World_Cup -O 2014_FIFA_World_Cup.html
wget -q en.wikipedia.org/wiki/2014_FIFA_World_Cup_squads -O 2014_FIFA_World_Cup_squads.html

#Need this for non-ASCII characters (player names)
export PYTHONIOENCODING=UTF-8

result_dir=../static/data/results
./all_players_bs4.py > $result_dir/all_players.txt
./group_ranks_bs4.py > $result_dir/group_ranks.txt
./goalscorers_bs4.py > $result_dir/goalscorers.txt
./shutouts_bs4.py > $result_dir/shutouts.txt

sed -i "s/Ivory Coast/Côte d'Ivoire/g" $result_dir/group_ranks.txt
sed -i "s/Ivory Coast/Côte d'Ivoire/g" $result_dir/shutouts.txt 

sed -i "s/Bosnia and Herzegovina/Bosnia-Herzegovina/g" $result_dir/group_ranks.txt
sed -i "s/Bosnia and Herzegovina/Bosnia-Herzegovina/g" $result_dir/shutouts.txt 

sed -i "s/Jorge Valdivia/Jorge Valdívia/g" $result_dir/goalscorers.txt
sed -i "s/Jorge Valdivia/Jorge Valdívia/g" $result_dir/all_players.txt 

sed -i "s/Juan Quintero/Juan Fernando Quintero/g" $result_dir/goalscorers.txt
sed -i "s/Juan Quintero/Juan Fernando Quintero/g" $result_dir/all_players.txt 

sed -i "s/Lee Keun-ho/Lee Keun-Ho/g" $result_dir/goalscorers.txt
sed -i "s/Lee Keun-ho/Lee Keun-Ho/g" $result_dir/all_players.txt
