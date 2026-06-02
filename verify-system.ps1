$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = 'python'
$verify = Join-Path $root 'tools\verify_daily_shelf.py'
$fallbackWorkflow = Join-Path $root '.github\workflows\daily-shelf.yml'
$taskName = 'HUMANi Daily Autodigital Shelf'
$watchdogTaskName = 'HUMANi Daily Autodigital Shelf Watchdog'

Set-Location $root
if (-not (Test-Path -LiteralPath $fallbackWorkflow)) {
    throw "Missing GitHub fallback workflow: $fallbackWorkflow"
}

$fallbackWorkflowText = Get-Content -LiteralPath $fallbackWorkflow -Raw
foreach ($needle in @(
    'Daily Autodigital Shelf Fallback',
    'contents: write',
    'America/New_York',
    'tools/generate_daily_shelf.py --date',
    'tools/verify_daily_shelf.py --date',
    'tools/submit_indexnow.py',
    'tools/submit_calmsprout_indexnow.py',
    'git diff --cached --quiet'
)) {
    if (-not $fallbackWorkflowText.Contains($needle)) {
        throw "GitHub fallback workflow missing expected text: $needle"
    }
}

$runDailyText = Get-Content -LiteralPath (Join-Path $root 'run-daily.ps1') -Raw
foreach ($needle in @(
    'tools\submit_calmsprout_indexnow.py',
    'CalmSprout IndexNow submission complete'
)) {
    if (-not $runDailyText.Contains($needle)) {
        throw "Daily run wrapper missing expected text: $needle"
    }
}

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
