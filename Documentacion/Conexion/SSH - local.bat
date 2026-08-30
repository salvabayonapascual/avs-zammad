@echo off
REM Abrir PowerShell y ejecutar el comando SSH
powershell -NoExit -Command "ssh root@192.168.150.186 -p 22"
REM powershell -NoExit -Command "ssh -i 'id.pub' root@192.168.150.181 -p 22"

exit
