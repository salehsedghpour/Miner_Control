#!/bin/bash
#(cd /opt/MinerControl/app ;git reset --hard;git remote add origin "https://github.com/salehsedghpour/miner_control";git pull origin master)
username=$( awk -F "=" '/username/ {print $2}' /opt/MinerControl/config.ini)
secret=$( awk -F "=" '/secret/ {print $2}' /opt/MinerControl/config.ini)
(cd /opt/MinerControl/worker ;git reset --hard;git remote add origin "http://$username:$secret@mon.hcsone.ir:8929/$username/workers.git";git config --global user.email "$username@mon.hcsone.ir";git config --global user.name "$username";git config credential.helper store --file=/opt/MinerControl/.git-credentials)