#!/bin/bash

#Find directory this script is stored in.
#Cribbed from: http://stackoverflow.com/questions/59895/can-a-bash-script-tell-what-directory-its-stored-in
#N.B. May not work when symlinks are involved
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#Change script directory
cd ${SCRIPT_DIR}

#Don't update database if update_results.sh fails
set -e
date >> update_vmgame_results.log

#Grab latest wikipedia and process
cd ext
./update_results.sh &>> ../update_vmgame_results.log
cd ../

echo "Starting update_vmgame_results.py" >> update_vmgame_results.log
#Go from text files to database
./update_vmgame_results.py &>> update_vmgame_results.log

echo "Done updating results" >> update_vmgame_results.log
