@echo off
setlocal enabledelayedexpansion

REM ============================================
REM Variables de configuración para MySQL
REM ============================================
set MYSQL_SERVICE=mysql_db
set MYSQL_USER=root
set MYSQL_PASSWORD="1234"
set SQL_FILE=Proyecto\DB\init.sql

echo ===================================================
echo Script de inicialización de base de datos MySQL
echo ===================================================

REM ============================================
REM Verificación de instalación de Docker
REM Comprueba si el comando 'docker' está disponible en el sistema
REM ============================================
where docker >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker no está instalado o no está en el PATH.
    exit /b 1
)

REM ============================================
REM Verificación de que el servicio Docker esté activo
REM Intenta obtener información de Docker para confirmar que el daemon está corriendo
REM ============================================
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker está instalado pero el servicio no está activo.
    exit /b 1
)

REM ============================================
REM Detección automática de la versión de Docker Compose
REM Busca primero 'docker compose' (v2) y luego 'docker-compose' (v1)
REM ============================================
set COMPOSE_CMD=
docker compose version >nul 2>&1
if %errorlevel%==0 (
    set COMPOSE_CMD=docker compose
    goto compose_found
)

docker-compose version >nul 2>&1
if %errorlevel%==0 (
    set COMPOSE_CMD=docker-compose
    goto compose_found
)

echo [ERROR] No se encontró docker compose ni docker-compose.
exit /b 1

:compose_found

REM ============================================
REM Inicio de los contenedores Docker
REM Ejecuta docker compose up en modo detached (background)
REM ============================================
echo.
echo Iniciando contenedores con %COMPOSE_CMD%...
%COMPOSE_CMD% up -d
if errorlevel 1 (
    echo [ERROR] Fallo al levantar los contenedores.
    exit /b 1
)

REM ============================================
REM Espera activa hasta que MySQL esté completamente disponible
REM Utiliza mysqladmin ping para verificar que el servidor responda
REM ============================================
echo.
echo Esperando a que MySQL esté disponible...

:wait_mysql
docker exec %MYSQL_SERVICE% mysqladmin ping -h localhost -u%MYSQL_USER% -p%MYSQL_PASSWORD% --silent >nul 2>nul
if errorlevel 1 (
    timeout /t 2 >nul
    goto wait_mysql
)

echo MySQL está listo.

REM ============================================
REM Ejecución del script SQL de inicialización
REM Si existe el archivo init.sql, lo ejecuta dentro del contenedor MySQL
REM ============================================
if not exist "%SQL_FILE%" (
    echo [ADVERTENCIA] No se encontró el archivo SQL en %SQL_FILE%
    goto test_connection
)

echo Ejecutando script SQL de inicialización: %SQL_FILE%
type "%SQL_FILE%" | docker exec -i %MYSQL_SERVICE% mysql -u%MYSQL_USER% -p%MYSQL_PASSWORD%
if errorlevel 1 (
    echo [ERROR] Error al ejecutar el script SQL.
    exit /b 1
)

echo Script SQL ejecutado correctamente.

:test_connection

REM ============================================
REM Prueba final de conexión a MySQL
REM Verifica una vez más que MySQL responde correctamente
REM ============================================
echo.
echo Probando conexión a MySQL...
docker exec %MYSQL_SERVICE% mysqladmin ping -hlocalhost -u%MYSQL_USER% -p%MYSQL_PASSWORD%
if errorlevel 1 (
    echo [ERROR] Fallo en la prueba de conexión.
    exit /b 1
)

echo.
echo [ÉXITO] Conexión OK. Sistema listo para usar.

endlocal
