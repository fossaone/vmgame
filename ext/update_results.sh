#!/bin/bash

#Quit on failure
set -e

#NOTE: Not updating players anymore
echo "Start downloading wikipedia page"
wget -q https://en.wikipedia.org/wiki/UEFA_Euro_2016 -O UEFA_Euro_2016.html
echo "Done downloading wikipedia page"
wget_err=$?
if [ "$wget_err" -ne "0" ]
then
    echo "wget failed with error code $wget_err"
    exit 1
fi

#Need this for non-ASCII characters (player names)
export PYTHONIOENCODING=UTF-8

echo "Start beautiful soup"
result_dir=../static/data/results

#Turn this off once we are sure squads are final
#wget -q https://en.wikipedia.org/wiki/UEFA_Euro_2016_squads -O UEFA_Euro_2016_squads.html
#./all_players_bs4.py > $result_dir/all_players.txt
#./group_ranks_bs4.py > $result_dir/group_ranks.txt
#no goalscorers yet
#./goalscorers_bs4.py > $result_dir/goalscorers.txt
#./shutouts_bs4.py > $result_dir/shutouts.txt
./knockout_stage_bs4.py > $result_dir/knockout_stage.txt

#Old fixup code in case we need to update
#echo "Start fix-up country names"
#sed -i "s/Ivory Coast/Côte d'Ivoire/g" $result_dir/group_ranks.txt
#sed -i "s/Ivory Coast/Côte d'Ivoire/g" $result_dir/shutouts.txt
#sed -i "s/Ivory Coast/Côte d'Ivoire/g" $result_dir/knockout_stage.txt

#sed -i "s/Bosnia and Herzegovina/Bosnia-Herzegovina/g" $result_dir/group_ranks.txt
#sed -i "s/Bosnia and Herzegovina/Bosnia-Herzegovina/g" $result_dir/shutouts.txt
#sed -i "s/Bosnia and Herzegovina/Bosnia-Herzegovina/g" $result_dir/knockout_stage.txt

#Wikipedia refuses to use a consistent name for this guy
# I changed the name in the db on pythonanywhere
#sed -i "s/Georgios Samaras/Giorgos Samaras/g" $result_dir/goalscorers.txt

echo "Done update_results.sh"
