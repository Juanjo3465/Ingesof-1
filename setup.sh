#!/bin/bash
set -e

# Variables de configuración para la conexión a MySQL
MYSQL_SERVICE="mysql-db"
MYSQL_USER="root"
MYSQL_PASSWORD="1234"
SQL_FILE="Proyecto/DB/init.sql"

# Verificación de instalación de Docker
# Comprueba si el comando 'docker' está disponible en el sistema
if ! command -v docker >/dev/null 2>&1; then
  echo "Docker no está instalado o no está en el PATH."
  echo "Instálalo desde https://docs.docker.com/get-docker/"
  exit 1
fi

# Verificación de que el servicio Docker esté activo
# Intenta obtener información de Docker para confirmar que el daemon está corriendo
if ! docker info >/dev/null 2>&1; then
  echo "Docker está instalado pero el servicio no está activo."
  echo "Asegúrate de que Docker Desktop o el daemon esté en ejecución."
  exit 1
fi

# Detección automática de la versión de Docker Compose
# Busca si está disponible 'docker compose' (v2) o 'docker-compose' (v1)
if command -v docker compose >/dev/null 2>&1; then
    COMPOSE_CMD="docker compose"
elif command -v docker-compose >/dev/null 2>&1; then
    COMPOSE_CMD="docker-compose"
else
    echo "No se encontró docker compose."
    exit 1
fi

# Inicio de los contenedores Docker
# Ejecuta docker compose up en modo detached (background)
echo "Levantando contenedores..."
$COMPOSE_CMD up -d

# Espera activa hasta que MySQL esté completamente disponible
# Utiliza mysqladmin ping para verificar que el servidor responda
echo "Esperando a que MySQL esté disponible..."
until docker exec "$MYSQL_SERVICE" mysqladmin ping -h"localhost" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" --silent; do
  sleep 2
done
echo "MySQL está listo."

# Ejecución del script SQL de inicialización
# Si existe el archivo init.sql, lo ejecuta dentro del contenedor MySQL
if [ -f "$SQL_FILE" ]; then
  echo "Ejecutando script SQL de inicialización: $SQL_FILE"
  docker exec -i "$MYSQL_SERVICE" mysql -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" < "$SQL_FILE"
  echo "Script ejecutado correctamente."
else
  echo "No se encontró el archivo SQL en $SQL_FILE"
fi

echo ""

# Prueba final de conexión a MySQL
# Verifica una vez más que MySQL responde correctamente
echo "Probando conexión a MySQL..."
docker exec "$MYSQL_SERVICE" mysqladmin ping -h"localhost" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD"

echo ""
echo "Conexión OK."

