#!/bin/bash

LOG_FILE="logs/run_experimento.log"
API_URL="http://api-consulta-principal:8090/consulta"

for i in {1..10}
do
  RESPONSE=$(curl -s $API_URL)
  TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
  echo "$TIMESTAMP - Call $i: $RESPONSE" >> $LOG_FILE
done