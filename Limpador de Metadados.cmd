@echo off
rem Aura Engine - Limpador de Metadados (Windows). De 2 cliques para abrir.
cd /d "%~dp0"
where node >nul 2>nul
if errorlevel 1 (
  echo Node.js nao encontrado. Instale com: winget install OpenJS.NodeJS.LTS
  pause
  exit /b 1
)
node "tools\limpador-de-metadados\app.js"
pause
