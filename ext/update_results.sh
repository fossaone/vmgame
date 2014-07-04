#!/bin/bash

#Quit on failure
set -e

#NOTE: Not updating players anymore
echo "Start downloading wikipedia page"
wget -q http://en.wikipedia.org/wiki/2014_FIFA_World_Cup -O 2014_FIFA_World_Cup.html
echo "Done downloading wikipedia page"
wget_err=$?
if [ "$wget_err" -ne "0" ]
then
    echo "wget failed with error code $wget_err"
    exit 1
fi
#wget -q en.wikipedia.org/wiki/2014_FIFA_World_Cup_squads -O 2014_FIFA_World_Cup_squads.html

#Need this for non-ASCII characters (player names)
export PYTHONIOENCODING=UTF-8

echo "Start beautiful soup"
result_dir=../static/data/results
#./all_players_bs4.py > $result_dir/all_players.txt
./group_ranks_bs4.py > $result_dir/group_ranks.txt
./goalscorers_bs4.py > $result_dir/goalscorers.txt
./shutouts_bs4.py > $result_dir/shutouts.txt
./knockout_stage_bs4.py > $result_dir/knockout_stage.txt

echo "Start fix-up country names"
sed -i "s/Ivory Coast/Côte d'Ivoire/g" $result_dir/group_ranks.txt
sed -i "s/Ivory Coast/Côte d'Ivoire/g" $result_dir/shutouts.txt 
sed -i "s/Ivory Coast/Côte d'Ivoire/g" $result_dir/knockout_stage.txt

sed -i "s/Bosnia and Herzegovina/Bosnia-Herzegovina/g" $result_dir/group_ranks.txt
sed -i "s/Bosnia and Herzegovina/Bosnia-Herzegovina/g" $result_dir/shutouts.txt 
sed -i "s/Bosnia and Herzegovina/Bosnia-Herzegovina/g" $result_dir/knockout_stage.txt

#Wikipedia refuses to use a consistent name for this guy
# I changed the name in the db on pythonanywhere
#sed -i "s/Georgios Samaras/Giorgos Samaras/g" $result_dir/goalscorers.txt

echo "Done update_results.sh"
