@echo off
rem Aura Engine - Limpador de Metadados (Windows). De 2 cliques para abrir.
rem Funciona na raiz da Aura (onde o hook de inicio de sessao deixa uma copia)
rem e na pasta original, tools\limpador-de-metadados\lancadores\.
setlocal
set "APP=%~dp0tools\limpador-de-metadados\app.js"
if not exist "%APP%" set "APP=%~dp0..\app.js"
where node >nul 2>nul
if errorlevel 1 (
  echo Node.js nao encontrado. Instale com: winget install OpenJS.NodeJS.LTS
  pause
  exit /b 1
)
node "%APP%"
pause
