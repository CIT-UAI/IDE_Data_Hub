@echo off
chcp 65001 >nul
title CIT-UAI - Monitor de Consultas y Aprendizaje Activo
echo ===============================================================================
echo   CIT-UAI · MONITOR DE TELEMETRÍA Y CONSULTAS CIUDADANAS
echo   Centro de Inteligencia Territorial · Universidad Adolfo Ibáñez
echo ===============================================================================
echo.
python "%~dp0analizar_consultas_y_aprendizaje.py"
echo.
pause
