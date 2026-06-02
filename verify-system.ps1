$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = 'python'
$verify = Join-Path $root 'tools\verify_daily_shelf.py'
$taskName = 'HUMANi Daily Autodigital Shelf'

Set-Location $root
& $python $verify --live-url 'https://x26dotapp.github.io/daily-autodigital-shelf/'
if ($LASTEXITCODE -ne 0) {
    throw "Daily shelf verifier failed with exit code $LASTEXITCODE"
}

$task = Get-ScheduledTask -TaskName $taskName -ErrorAction Stop
$info = Get-ScheduledTaskInfo -TaskName $taskName -ErrorAction Stop

[pscustomobject]@{
    TaskName = $task.TaskName
    State = $task.State
    LastRunTime = $info.LastRunTime
    LastTaskResult = $info.LastTaskResult
    NextRunTime = $info.NextRunTime
}
