@echo off
setlocal enabledelayedexpansion
title CIT-UAI -- Publicador de Produccion IDE CIT
color 0B

echo ==============================================================================
echo   CIT-UAI :: DESPLIEGUE A PRODUCCION IDE CIT
echo   Centro de Inteligencia Territorial - Universidad Adolfo Ibanez
echo ==============================================================================
echo Destino AWS S3: s3://ide.cit.uai.cl
echo Region AWS:     us-east-1
echo.

set /p CONFIRM="Esta seguro de sincronizar y publicar a produccion? (S/N): "
if /i not "!CONFIRM!"=="S" (
    echo Despliegue cancelado por el usuario.
    exit /b 0
)

echo.
echo [1/3] Empaquetando y validando release de produccion...
python "%~dp0desplegador_ide_produccion.py" --build-only
if %ERRORLEVEL% neq 0 (
    echo Error durante el empaquetado. Abortando.
    pause
    exit /b 1
)

echo.
echo [2/3] Sincronizando activos estaticos con AWS S3 (cache inmutable)...
aws s3 sync "%~dp0dist" "s3://ide.cit.uai.cl" --delete --region us-east-1 --exclude "*.html" --exclude "manifest.json" --exclude "sitemap.xml" --exclude "robots.txt" --cache-control "public, max-age=31536000, immutable"

echo.
echo [3/3] Sincronizando paginas HTML y manifiesto (sin cache para actualizacion inmediata)...
aws s3 cp "%~dp0dist\index.html" "s3://ide.cit.uai.cl/index.html" --region us-east-1 --cache-control "max-age=0, no-cache, no-store, must-revalidate" --content-type "text/html; charset=utf-8"
aws s3 cp "%~dp0dist\descargas-2017.html" "s3://ide.cit.uai.cl/descargas-2017.html" --region us-east-1 --cache-control "max-age=0, no-cache, no-store, must-revalidate" --content-type "text/html; charset=utf-8"
aws s3 cp "%~dp0dist\guia-tecnica.html" "s3://ide.cit.uai.cl/guia-tecnica.html" --region us-east-1 --cache-control "max-age=0, no-cache, no-store, must-revalidate" --content-type "text/html; charset=utf-8"
aws s3 cp "%~dp0dist\red-ides.html" "s3://ide.cit.uai.cl/red-ides.html" --region us-east-1 --cache-control "max-age=0, no-cache, no-store, must-revalidate" --content-type "text/html; charset=utf-8"
aws s3 cp "%~dp0dist\sitemap.xml" "s3://ide.cit.uai.cl/sitemap.xml" --region us-east-1 --cache-control "public, max-age=86400, must-revalidate" --content-type "application/xml"
aws s3 cp "%~dp0dist\robots.txt" "s3://ide.cit.uai.cl/robots.txt" --region us-east-1 --cache-control "public, max-age=86400, must-revalidate" --content-type "text/plain"
aws s3 cp "%~dp0dist\manifest.json" "s3://ide.cit.uai.cl/manifest.json" --region us-east-1 --cache-control "max-age=0, no-cache, no-store, must-revalidate" --content-type "application/json"

echo.
echo ==============================================================================
echo   PUBLICACION COMPLETADA CON EXITO
echo   Portal disponible en: https://ide.cit.uai.cl
echo ==============================================================================
pause
