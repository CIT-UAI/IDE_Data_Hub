@echo off
chcp 65001 >nul
title IDE CIT — Servidor Local de Previsualización (Puerto 8080)
color 0B

echo ===============================================================================
echo  🌐 IDE CIT — LANZADOR LOCAL DE PREVISUALIZACIÓN Y PRUEBAS
echo  Centro de Inteligencia Territorial (CIT-UAI) · Universidad Adolfo Ibáñez
echo ===============================================================================
echo.
echo [1/3] Verificando compilación del portal web...
python "%~dp0generador_portal_ide_cit.py"
if %errorlevel% neq 0 (
    echo [ERROR] Falló la compilación de index.html.
    pause
    exit /b 1
)

echo.
echo [2/3] Abriendo navegador web en http://localhost:8080/index.html ...
start "" "http://localhost:8080/index.html"

echo.
echo [3/3] Iniciando servidor HTTP local en puerto 8080...
echo Presiona Ctrl+C para detener el servidor.
echo.
cd /d "%~dp0"
python -m http.server 8080

pause
