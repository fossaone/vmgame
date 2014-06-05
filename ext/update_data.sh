#!/bin/bash

testing=1

if [ ! -d world-cup ]
then
  git clone https://github.com/openfootball/world-cup.git
fi

cd world-cup
if [ $testing -eq 1 ] 
then
  echo "Not updating from source during testing."
else
  git pull origin
fi


curr_cup="2014--brazil"
data_dir=../../static/data

#curr_squads=`ls ${curr_cup}/squads/*.txt`
#Using blessed data
curr_squads=`ls ../final_squads/*.txt`
#Process to be usable
for sq in $curr_squads
do
  #dos2unix -q $sq
  #First get the pretty country name
  country=`basename $sq | sed 's/^..\-//' | sed 's/\.txt$//'`
  #Replace " and " with "-" for Boznia and Herzegovina
  head -2 $sq | tail -1 | sed "s/#/%/" | sed "s/\ and\ /-/g" > $data_dir/${country}-players.txt
  egrep 'Defenders|Goal Keepers|Midfielders|Forwards|^[A-Z]' $sq \
      | sed 's/^\(..*\)\ *##.*/\1/' | sed 's/\ *(captain)//' \
      >> $data_dir/${country}-players.txt
done

#Note special character "|" (not a pipe)
for gr in A B C D E F G H
do
  group_name="Group-${gr}"
  #Replacing two or more spaces by a pipe because some countries have multi-word names
  group_teams=`grep "^Group ${gr}  |" ${curr_cup}/cup.txt | sed "s/Group ${gr}....//" | sed "s/\ \ \ */|/g"`
  echo $group_teams > $data_dir/$group_name.txt
done

