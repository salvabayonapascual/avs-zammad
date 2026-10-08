param([switch]$CheckOnly)
$ErrorActionPreference = 'Stop'
$rclonePath = Join-Path $env:LOCALAPPDATA 'AVS\Tools\rclone\rclone.exe'
$identityPath = Join-Path $env:USERPROFILE '.ssh\id_ed25519_zammad_sftp'
$knownHostsPath = Join-Path $env:USERPROFILE '.ssh\known_hosts_zammad_sftp'
foreach ($requiredPath in @($rclonePath, $identityPath, $knownHostsPath)) {
    if (-not (Test-Path -LiteralPath $requiredPath -PathType Leaf)) {
        throw "Falta un requisito local: $requiredPath"
    }
}
# Remote inline: no elimina ni reescribe remotes existentes ni otras unidades.
$connectionArgs = @('--config', 'NUL', '--sftp-host', '192.168.150.186', '--sftp-user', 'root',
    '--sftp-port', '22', '--sftp-key-file', $identityPath,
    '--sftp-known-hosts-file', $knownHostsPath, '--contimeout', '10s', '--timeout', '20s')
& $rclonePath lsd ':sftp:/' @connectionArgs | Out-Null
if ($LASTEXITCODE -ne 0) { throw 'No se ha podido validar el acceso SFTP.' }
if ($CheckOnly) { Write-Output 'SFTP verificado; identidad dedicada y host conocido.'; exit 0 }
$winFspDll = Join-Path ${env:ProgramFiles(x86)} 'WinFsp\bin\winfsp-x64.dll'
if (-not (Test-Path -LiteralPath $winFspDll)) {
    throw 'Acceso SFTP correcto. Para montar Z: falta instalar WinFsp (controlador de Windows).'
}
if (Test-Path -LiteralPath 'Z:\') {
    throw 'Z: ya esta ocupada; no se desmonta ni sustituye una unidad existente.'
}
$logPath = Join-Path $env:LOCALAPPDATA 'AVS\Tools\rclone\zammad-mount.log'
$mountArgs = @('mount', ':sftp:/', 'Z:', '--vfs-cache-mode', 'full', '--links',
    '--log-file', $logPath) + $connectionArgs
# Start-Process necesita comillas explicitas para rutas con espacios.
$quotedArgs = ($mountArgs | ForEach-Object { '"' + $_ + '"' }) -join ' '
$mountProcess = Start-Process -FilePath $rclonePath -ArgumentList $quotedArgs -WindowStyle Hidden -PassThru
for ($attempt = 0; $attempt -lt 20; $attempt++) {
    Start-Sleep -Milliseconds 500
    if ($mountProcess.HasExited) { throw "El montaje fallo; consultar $logPath" }
    if (Test-Path -LiteralPath 'Z:\') {
        Start-Process explorer.exe -ArgumentList 'Z:\'
        exit 0
    }
}
throw "Montaje iniciado pero Z: no responde; consultar $logPath"
