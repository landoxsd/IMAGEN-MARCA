@echo off
title Procesador de Imagenes - MARCA IMAGEN
color 0A

echo ==============================================================
echo        INICIANDO PROCESADOR DE IMAGENES CON LOGO
echo ==============================================================
echo.

:: 1. Verificar si Python esta instalado
echo [Paso 1/3] Verificando instalacion de Python...
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    color 0C
    echo [ERROR CRITICO] Python no esta instalado o no esta agregado a las variables de entorno (PATH).
    echo Por favor instala Python desde la Microsoft Store o desde python.org
    echo Asegurate de marcar la casilla "Add python.exe to PATH" durante la instalacion.
    echo.
    pause
    exit /b
)
echo Python detectado correctamente.
echo.

:: 2. Instalar y verificar requerimientos
echo [Paso 2/3] Verificando dependencias (Pillow, customtkinter)...
pip install -r requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    color 0E
    echo [ADVERTENCIA] Hubo un problema al verificar los requerimientos, pero intentaremos continuar.
) ELSE (
    echo Dependencias actualizadas y listas.
)
echo.

:: 3. Ejecutar el programa principal
echo [Paso 3/3] Abriendo la interfaz grafica...
echo.
python main.py

:: Mantener la consola abierta en caso de que ocurra un error fatal en main.py
IF %ERRORLEVEL% NEQ 0 (
    color 0C
    echo.
    echo El programa se cerro inesperadamente. Revisa los errores de arriba.
    pause
)
