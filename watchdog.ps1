$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$logDir = Join-Path $root 'logs'
$stateDir = Join-Path $root 'state'
$logPath = Join-Path $logDir 'watchdog.log'
$statusPath = Join-Path $stateDir 'watchdog-status.json'
$runScript = Join-Path $root 'run-daily.ps1'
$verifyScript = Join-Path $root 'verify-system.ps1'
$installTaskScript = Join-Path $root 'install-scheduled-task.ps1'
$dailyTaskName = 'HUMANi Daily Autodigital Shelf'

New-Item -ItemType Directory -Force -Path $logDir | Out-Null
New-Item -ItemType Directory -Force -Path $stateDir | Out-Null

function Write-WatchdogLog {
    param([string]$Message)
    $line = '{0} {1}' -f (Get-Date).ToString('s'), $Message
    Add-Content -Path $logPath -Value $line -Encoding UTF8
    Write-Output $line
}

function Save-WatchdogStatus {
    param(
        [string]$Status,
        [string]$Message,
        [int]$Failures,
        [int]$RepairAttempts
    )

    $payload = [ordered]@{
        checked_at = (Get-Date).ToUniversalTime().ToString('s') + 'Z'
        status = $Status
        message = $Message
        failures = $Failures
        repair_attempts = $RepairAttempts
        daily_task = $dailyTaskName
    }
    $payload | ConvertTo-Json -Depth 4 | Set-Content -Path $statusPath -Encoding UTF8
}

function Ensure-DailyTask {
    try {
        Get-ScheduledTask -TaskName $dailyTaskName -ErrorAction Stop | Out-Null
        return $false
    }
    catch {
        Write-WatchdogLog "Daily task missing; reinstalling $dailyTaskName."
        & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $installTaskScript | Out-Null
        return $true
    }
}

function Invoke-Verify {
    $output = & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $verifyScript 2>&1
    $exitCode = $LASTEXITCODE
    foreach ($line in $output) {
        Add-Content -Path $logPath -Value ('{0} verify-system: {1}' -f (Get-Date).ToString('s'), $line) -Encoding UTF8
    }
    if ($null -eq $exitCode) {
        return 0
    }
    return [int]$exitCode
}

Set-Location $root
Write-WatchdogLog 'Daily Autodigital Shelf watchdog starting.'

$failures = 0
$repairAttempts = 0
$taskReinstalled = Ensure-DailyTask
if ($taskReinstalled) {
    $repairAttempts += 1
}

$verifyExit = Invoke-Verify
if ($verifyExit -ne 0) {
    $failures += 1
    $repairAttempts += 1
    Write-WatchdogLog "Verifier returned exit code $verifyExit; running daily generator/publisher."
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $runScript
    if ($LASTEXITCODE -ne 0) {
        $failures += 1
        Save-WatchdogStatus -Status 'failed' -Message "run-daily.ps1 returned exit code $LASTEXITCODE" -Failures $failures -RepairAttempts $repairAttempts
        throw "run-daily.ps1 returned exit code $LASTEXITCODE"
    }

    $verifyExit = Invoke-Verify
    if ($verifyExit -ne 0) {
        $failures += 1
        Save-WatchdogStatus -Status 'failed' -Message "Verifier still returned exit code $verifyExit after repair attempt" -Failures $failures -RepairAttempts $repairAttempts
        throw "Verifier still returned exit code $verifyExit after repair attempt"
    }
}

Save-WatchdogStatus -Status 'ok' -Message 'Verifier passed and daily task is present.' -Failures $failures -RepairAttempts $repairAttempts
Write-WatchdogLog 'Daily Autodigital Shelf watchdog complete.'
