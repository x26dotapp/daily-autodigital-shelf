$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$taskName = 'HUMANi Daily Autodigital Shelf'
$runScript = Join-Path $root 'run-daily.ps1'

if (-not (Test-Path -LiteralPath $runScript)) {
    throw "Missing run script: $runScript"
}

$action = New-ScheduledTaskAction `
    -Execute 'powershell.exe' `
    -Argument ('-NoProfile -ExecutionPolicy Bypass -File "{0}"' -f $runScript) `
    -WorkingDirectory $root

$trigger = New-ScheduledTaskTrigger -Daily -At 6:10am
$settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -MultipleInstances IgnoreNew

$principal = New-ScheduledTaskPrincipal `
    -UserId ("{0}\{1}" -f $env:USERDOMAIN, $env:USERNAME) `
    -LogonType Interactive `
    -RunLevel LeastPrivilege

Register-ScheduledTask `
    -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Principal $principal `
    -Description 'Generates and publishes the Daily Autodigital Shelf static site once per day.' `
    -Force | Out-Null

Write-Output "Installed scheduled task: $taskName"
