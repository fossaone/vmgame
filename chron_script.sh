#!/bin/bash

#Don't update database if update_results.sh fails
set -e

#Grab latest wikipedia and process
cd ext
./update_results.sh
cd ../

#Go from text files to database
./update_vmgame_results.py


