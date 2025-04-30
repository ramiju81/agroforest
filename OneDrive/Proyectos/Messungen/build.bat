@echo off
REM --------------------------------------------------
REM Generador seguro de .exe para Flask/Python
REM --------------------------------------------------

echo Verificando PyInstaller...
python -m pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ PyInstaller no está instalado. Instalando...
    python -m pip install pyinstaller
)

echo.
echo Limpiando compilaciones anteriores...
if exist dist\app.exe (
    del /q dist\app.exe
    if %errorlevel% neq 0 (
        echo ❌ No se pudo eliminar el .exe anterior
        pause
        exit /b 1
    )
)

echo.
echo Compilando aplicación...
pyinstaller --onefile --icon=static\img\logo.ico --windowed --noconfirm app.py

echo.
if exist dist\app.exe (
    echo ✅ ¡Éxito! Ejecutable generado en:
    echo %cd%\dist\app.exe
    timeout /t 3
    explorer %cd%\dist
) else (
    echo ❌ Error: No se generó el archivo .exe
    echo Revise los mensajes de error arriba
)

pause