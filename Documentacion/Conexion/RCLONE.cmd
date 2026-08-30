@echo off
::.\rclone.exe rcd --rc-web-gui

net use Z: /delete /y
cd /d C:\Datos\Conexiones\rclone

REM === Crear o actualizar remote ZammadAVS ===
.\rclone.exe config delete ZammadAVS >nul 2>&1
.\rclone.exe config create ZammadAVS sftp host=zammad.avsconsulting.es user=root port=22 key_file=%userprofile%\.ssh\id_rsa use_insecure_cipher=false

REM === Montar remote en segundo plano en unidad Z: ===
start "Montar ZammadAVS" cmd /c ".\rclone.exe mount ZammadAVS:\ Z: --vfs-cache-mode full --links"

REM === Esperar un poco a que monte (ajustar si necesario) ===
timeout /t 3 >nul

REM === Abrir unidad Z: en el explorador ===
start Z:\


