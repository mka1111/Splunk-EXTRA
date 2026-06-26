#!/bin/bash


generate_random_log_line() {

  local line="$1"
  echo "function  : $line" 

  # time range: last 7 days
  local START_EPOCH=$((END - 604800))  # 7 * 24 * 60 * 60
  local END_EPOCH=$(date +%s)





# pick random timestamp in range
RAND_EPOCH=$((START + RANDOM % (END_EPOCH - START_EPOCH)))

  # format like syslog: "Jun 20 10:36:29"
  local RAND_DATE=$(date -d "@$RAND_EPOCH" "+%b %d %H:%M:%S")

  # remove original timestamp (first 15–16 chars)
  local BODY=$(echo "$line" | sed 's/^[A-Za-z]\{3\} [ 0-9][0-9] [0-9:]\{8\} //')

  # return new line
  echo "$RAND_DATE $BODY"
}




TIME=10
MODE="filel"

while getopts "t:m:o:d:i:p:l:f:" option
do
    case "$option" in
        t) TIME="$OPTARG" ;;
        i) IP="$OPTARG" ;;
        p) PORT="$OPTARG" ;;
        o) OUTPUT="$OPTARG" ;;
        d) DELAY="$OPTARG" ;;
        m) MODE="$OPTARG" ;;
        l) LOG_TYPE="$OPTARG" ;;
        f) NEW_FILE="$OPTARG" ;;
	
	*) echo "Usage: $0 [-t time] [-m mode] [-o output] [-d delay] [-l (netflow/syslog/cef) ] [-f new file]"; exit 1 ;;
    esac
done




echo "Running..."



echo "Time = $TIME"
echo "Mode = $MODE"
echo "Output = $OUTPUT" 
echo "Delay = $DELAY" 
# cef-100.log    net-flow-100.log  syslog-100.log


LOG_DIR="./"

case "$LOG_TYPE" in
  syslog) FILE="$LOG_DIR/examples/syslog-100.log" ;;
  netflow) FILE="$LOG_DIR/examples/net-flow-100.log" ;;
  cef) FILE="$LOG_DIR/examples/cef-100.log" ;;
esac



if [[ "$MODE" == "file" || "$MODE" == "ip" ]]; then
  

if [[ "$MODE" == "file" ]]; then
echo "jestem in file"


while IFS= read -r line; do
  echo "$line"  >> $NEW_FILE
  sleep "$DELAY"
done < "$FILE"





fi

if [[ "$MODE" == "ip" ]]; then

while IFS= read -r line; do
  echo "$line" | nc -w0 "$IP" "$PORT"
  sleep "$DELAY"
generate_random_log_line "$line"
done < "$FILE"
fi
  


else
  echo "-m must be file of ip "
  exit 1
fi




# sed -n $((RANDOM % `cat ip.lst | wc -l` + 1))p ip.lst
# show random ip from ip.lst
