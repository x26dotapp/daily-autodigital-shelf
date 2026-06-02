$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$logDir = Join-Path $root 'logs'
$logPath = Join-Path $logDir 'daily-run.log'
$scriptPath = Join-Path $root 'tools\generate_daily_shelf.py'
$verifyPath = Join-Path $root 'tools\verify_daily_shelf.py'

New-Item -ItemType Directory -Force -Path $logDir | Out-Null

function Write-RunLog {
    param([string]$Message)
    $line = '{0} {1}' -f (Get-Date).ToString('s'), $Message
    Add-Content -Path $logPath -Value $line -Encoding UTF8
    Write-Output $line
}

function Get-Python {
    $candidates = @(
        'C:\Users\ash2inf3rn0\AppData\Local\Programs\Python\Python312\python.exe',
        'python'
    )

    foreach ($candidate in $candidates) {
        try {
            $cmd = Get-Command $candidate -ErrorAction Stop
            return $cmd.Source
        }
        catch {
        }
    }

    throw 'Python was not found.'
}

Set-Location $root
Write-RunLog 'Daily Autodigital Shelf run starting.'

$python = Get-Python
& $python $scriptPath
if ($LASTEXITCODE -ne 0) {
    throw "Generator failed with exit code $LASTEXITCODE"
}

& $python $verifyPath --min-pack-count 21
if ($LASTEXITCODE -ne 0) {
    throw "Verifier failed with exit code $LASTEXITCODE"
}

if (Test-Path -LiteralPath (Join-Path $root '.git')) {
    git add docs state README.md config/config.example.json tools run-daily.ps1 install-scheduled-task.ps1 verify-system.ps1 .gitignore | Out-Null
    $status = git status --porcelain
    if ($status) {
        $stamp = Get-Date -Format 'yyyy-MM-dd'
        git commit -m "Daily shelf update $stamp" | Out-Null
        git push origin main | Out-Null
        Write-RunLog 'Committed and pushed site update.'
    }
    else {
        Write-RunLog 'No git changes to publish.'
    }
}
else {
    Write-RunLog 'No git repository found yet; generated files only.'
}

Write-RunLog 'Daily Autodigital Shelf run complete.'
