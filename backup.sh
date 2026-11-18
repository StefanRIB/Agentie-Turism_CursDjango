#!/bin/bash

DB_NAME="django_agentie_turism"
DB_USER="stefan"
APP_NAME="aplicatie_agentie_turism" 

echo "Se creează backup-ul cu instrucțiuni INSERT pentru tabelele proprii..."

# pg_dump extrage doar datele (--data-only) sub formă de comenzi insert (--column-inserts)
# Flag-ul -t filtrează doar tabelele aplicației mele
/Library/PostgreSQL/18/bin/pg_dump -U $DB_USER -h localhost -d $DB_NAME --data-only --column-inserts -t "${APP_NAME}_*" > backup_laborator.sql

echo "Backup finalizat! Datele au fost salvate în backup_laborator.sql."