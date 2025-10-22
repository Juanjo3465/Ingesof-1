#!/bin/bash
set -e

MYSQL_SERVICE="mysql-db"
MYSQL_USER="root"
MYSQL_PASSWORD="1234"
SQL_FILE="Proyecto/DB/init.sql"

# Verificar que Docker esté instalado
if ! command -v docker >/dev/null 2>&1; then
  echo "Docker no está instalado o no está en el PATH."
  echo "Instálalo desde https://docs.docker.com/get-docker/"
  exit 1
fi

# Verificar que Docker esté corriendo
if ! docker info >/dev/null 2>&1; then
  echo "Docker está instalado pero el servicio no está activo."
  echo "Asegúrate de que Docker Desktop o el daemon esté en ejecución."
  exit 1
fi

# Detectar versión de Compose
if command -v docker compose >/dev/null 2>&1; then
    COMPOSE_CMD="docker compose"
elif command -v docker-compose >/dev/null 2>&1; then
    COMPOSE_CMD="docker-compose"
else
    echo "No se encontró docker compose."
    exit 1
fi

echo "Levantando contenedores..."
$COMPOSE_CMD up -d

echo "Esperando a que MySQL esté disponible..."
until docker exec "$MYSQL_SERVICE" mysqladmin ping -h"localhost" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" --silent; do
  sleep 2
done
echo "MySQL está listo."

if [ -f "$SQL_FILE" ]; then
  echo "Ejecutando script SQL de inicialización: $SQL_FILE"
  docker exec -i "$MYSQL_SERVICE" mysql -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" < "$SQL_FILE"
  echo "Script ejecutado correctamente."
else
  echo "No se encontró el archivo SQL en $SQL_FILE"
fi

echo ""
echo "Probando conexión a MySQL..."
docker exec "$MYSQL_SERVICE" mysqladmin ping -h"localhost" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD"

echo ""
echo "Conexión OK."

