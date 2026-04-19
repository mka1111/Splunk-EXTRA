#!/bin/bash
echo 
echo " ==============================="
echo " ====   Search for $1    "
echo " ================================"
/bin/cat /home/mka/Desktop/knowlege_base.csv |  grep -oP "^$1,.*"
echo " ==============================="
