#!/bin/bash

LOG_FILE="logs/run_experimento.log"
API_URL="http://api-consulta-principal:8090/consulta"

log_message() {
  TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
  echo "$TIMESTAMP - $1" >> $LOG_FILE
}

echo "" > $LOG_FILE
log_message "Inicio Experimento"
for i in {1..10}
do
  RESPONSE=$(curl -s $API_URL)
  TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
  log_message "Call $i: $RESPONSE"
  sleep 1
done
log_message "Fin Experimento"