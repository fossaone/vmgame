#!/bin/bash

#For some reason pythonanywhere runs this from the home directory
cd /home/vmgame2014/vmgame

#Don't update database if update_results.sh fails
set -e
date >> update_vmgame_results.log

#Grab latest wikipedia and process
cd ext
./update_results.sh >> ../update_vmgame_results.log
cd ../

#Go from text files to database
./update_vmgame_results.py >> update_vmgame_results.log

