#!/bin/bash

#Find directory this script is stored in.
#Cribbed from: http://stackoverflow.com/questions/59895/can-a-bash-script-tell-what-directory-its-stored-in
#N.B. May not work when symlinks are involved
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#For some reason pythonanywhere runs this from the home directory
cd ${SCRIPT_DIR}

#Don't update database if update_results.sh fails
set -e
date >> update_vmgame_results.log

#Grab latest wikipedia and process
cd ext
./update_results.sh >> ../update_vmgame_results.log
cd ../

#Go from text files to database
./update_vmgame_results.py >> update_vmgame_results.log

sed -i -e '/^LAST_UPDATED.*/d' vmgame/config.py
echo "LAST_UPDATED = \"`date -u`\"" >> vmgame/config.py

