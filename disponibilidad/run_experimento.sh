#!/bin/bash

LOG_FILE="logs/run_experimento.log"
API_URL="http://api-consulta-principal:8090/consulta"

log_message() {
  echo "$1" >> $LOG_FILE
}

echo "" > $LOG_FILE
for experimento in $(seq 1 "$CANTIDAD_EXPERIMENTOS")
do
  for llamado in $(seq 1 "$PETICIONES_POR_EXPERIMENTO")
  do
    EVENT_TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
    log_message "$EVENT_TIMESTAMP | Experimento $experimento | Call $llamado | $(curl -s $API_URL)"
    sleep $DELAY_LLAMADO
  done
  sleep 5
done