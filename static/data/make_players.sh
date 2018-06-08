IFS=$'\n'
for team in `cat all_teams.txt`
do
grep "${team}" all_players.txt > "${team}-players.txt"
done
