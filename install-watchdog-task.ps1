$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$taskName = 'HUMANi Daily Autodigital Shelf Watchdog'
$watchdogScript = Join-Path $root 'watchdog.ps1'

if (-not (Test-Path -LiteralPath $watchdogScript)) {
    throw "Missing watchdog script: $watchdogScript"
}

$action = New-ScheduledTaskAction `
    -Execute 'powershell.exe' `
    -Argument ('-NoProfile -ExecutionPolicy Bypass -File "{0}"' -f $watchdogScript) `
    -WorkingDirectory $root

$trigger = New-ScheduledTaskTrigger -Daily -At 7:15am
$settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -MultipleInstances IgnoreNew

$principal = New-ScheduledTaskPrincipal `
    -UserId ("{0}\{1}" -f $env:USERDOMAIN, $env:USERNAME) `
    -LogonType Interactive `
    -RunLevel Limited

Register-ScheduledTask `
    -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Principal $principal `
    -Description 'Verifies the Daily Autodigital Shelf after the daily run and repairs safe local/publish drift.' `
    -Force | Out-Null

Write-Output "Installed scheduled task: $taskName"
