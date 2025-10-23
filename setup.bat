@echo off
setlocal enabledelayedexpansion

REM === CONFIGURACIÓN ===
set MYSQL_SERVICE=mysql_db
set MYSQL_USER=root
set MYSQL_PASSWORD=1234
set SQL_FILE=Proyecto\DB\init.sql


echo ===================================================
echo Script de inicialización de base de datos MySQL
echo ===================================================

REM === Verificar que Docker esté instalado ===
where docker >nul 2>&1
if errorlevel 1 (
    echo Docker no está instalado o no está en el PATH.
    echo Instálalo desde https://docs.docker.com/get-docker/
    exit /b 1
)

REM === Verificar que Docker esté corriendo ===
docker info >nul 2>&1
if errorlevel 1 (
    echo Docker está instalado pero el servicio no está activo.
    echo Asegúrate de que Docker Desktop o el daemon esté ejecutándose.
    exit /b 1
)

REM === Detectar si se usa docker compose o docker-compose ===
docker compose version >nul 2>&1
if %errorlevel%==0 (
    set COMPOSE_CMD=docker compose
) else (
    docker-compose version >nul 2>&1
    if %errorlevel%==0 (
        set COMPOSE_CMD=docker-compose
    ) else (
        echo No se encontró docker compose ni docker-compose.
        exit /b 1
    )
)

echo.
echo Iniciando contenedores con %COMPOSE_CMD%...
%COMPOSE_CMD% up -d

REM === Esperar hasta que MySQL responda ===

echo.
echo Esperando a que MySQL esté disponible...
:wait_mysql
docker exec %MYSQL_SERVICE% mysqladmin ping -h localhost -u%MYSQL_USER% -p%MYSQL_PASSWORD% --silent >nul 2>nul
if errorlevel 1 (
    timeout /t 2 >nul
    goto wait_mysql
)
echo MySQL está listo.

REM === Ejecutar script SQL de inicialización si existe ===
if exist "%SQL_FILE%" (
    echo Ejecutando script SQL de inicialización: %SQL_FILE%
    type "%SQL_FILE%" | docker exec -i %MYSQL_SERVICE% mysql -u%MYSQL_USER% -p%MYSQL_PASSWORD%
    if %errorlevel%==0 (
        echo Script SQL ejecutado correctamente.
    ) else (
        echo Error al ejecutar el script SQL.
    )
) else (
    echo No se encontró el archivo SQL en %SQL_FILE%
)


REM === Prueba final de conexión ===
echo.
echo Probando conexión a MySQL...
docker exec %MYSQL_SERVICE% mysqladmin ping -hlocalhost -u%MYSQL_USER% -p%MYSQL_PASSWORD%

echo.
echo Conexión OK.

endlocal