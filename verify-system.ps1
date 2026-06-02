$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = 'python'
$verify = Join-Path $root 'tools\verify_daily_shelf.py'
$taskName = 'HUMANi Daily Autodigital Shelf'
$watchdogTaskName = 'HUMANi Daily Autodigital Shelf Watchdog'

Set-Location $root
& $python $verify --min-pack-count 21 --live-url 'https://x26dotapp.github.io/daily-autodigital-shelf/'
if ($LASTEXITCODE -ne 0) {
    throw "Daily shelf verifier failed with exit code $LASTEXITCODE"
}

$task = Get-ScheduledTask -TaskName $taskName -ErrorAction Stop
$info = Get-ScheduledTaskInfo -TaskName $taskName -ErrorAction Stop
$watchdogTask = Get-ScheduledTask -TaskName $watchdogTaskName -ErrorAction Stop
$watchdogInfo = Get-ScheduledTaskInfo -TaskName $watchdogTaskName -ErrorAction Stop

[pscustomobject]@{
    TaskName = $task.TaskName
    State = $task.State
    LastRunTime = $info.LastRunTime
    LastTaskResult = $info.LastTaskResult
    NextRunTime = $info.NextRunTime
}

[pscustomobject]@{
    TaskName = $watchdogTask.TaskName
    State = $watchdogTask.State
    LastRunTime = $watchdogInfo.LastRunTime
    LastTaskResult = $watchdogInfo.LastTaskResult
    NextRunTime = $watchdogInfo.NextRunTime
}
