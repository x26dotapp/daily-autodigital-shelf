$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$logDir = Join-Path $root 'logs'
$logPath = Join-Path $logDir 'daily-run.log'
$scriptPath = Join-Path $root 'tools\generate_daily_shelf.py'
$verifyPath = Join-Path $root 'tools\verify_daily_shelf.py'
$supportMetricsPath = Join-Path $root 'tools\sync_support_metrics.py'
$downloadMetricsPath = Join-Path $root 'tools\sync_download_metrics.py'
$checkoutReadinessPath = Join-Path $root 'tools\sync_checkout_readiness.py'
$revenueProofPath = Join-Path $root 'tools\sync_revenue_proofs.py'
$indexNowPath = Join-Path $root 'tools\submit_indexnow.py'
$calmSproutIndexNowPath = Join-Path $root 'tools\submit_calmsprout_indexnow.py'

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
try {
    & $python $supportMetricsPath
    if ($LASTEXITCODE -eq 0) {
        Write-RunLog 'Support metrics sync complete.'
    }
    else {
        Write-RunLog "Support metrics sync returned exit code $LASTEXITCODE."
    }
}
catch {
    Write-RunLog "Support metrics sync failed: $($_.Exception.Message)"
}

try {
    & $python $downloadMetricsPath
    if ($LASTEXITCODE -eq 0) {
        Write-RunLog 'Download metrics sync complete.'
    }
    else {
        Write-RunLog "Download metrics sync returned exit code $LASTEXITCODE."
    }
}
catch {
    Write-RunLog "Download metrics sync failed: $($_.Exception.Message)"
}

try {
    & $python $checkoutReadinessPath
    if ($LASTEXITCODE -eq 0) {
        Write-RunLog 'Checkout readiness sync complete.'
    }
    else {
        Write-RunLog "Checkout readiness sync returned exit code $LASTEXITCODE."
    }
}
catch {
    Write-RunLog "Checkout readiness sync failed: $($_.Exception.Message)"
}

try {
    & $python $revenueProofPath
    if ($LASTEXITCODE -eq 0) {
        Write-RunLog 'Revenue proof sync complete.'
    }
    else {
        Write-RunLog "Revenue proof sync returned exit code $LASTEXITCODE."
    }
}
catch {
    Write-RunLog "Revenue proof sync failed: $($_.Exception.Message)"
}

& $python $scriptPath
if ($LASTEXITCODE -ne 0) {
    throw "Generator failed with exit code $LASTEXITCODE"
}

& $python $verifyPath --min-pack-count 29
if ($LASTEXITCODE -ne 0) {
    throw "Verifier failed with exit code $LASTEXITCODE"
}

if (Test-Path -LiteralPath (Join-Path $root '.git')) {
    git add docs state README.md config/config.example.json tools run-daily.ps1 watchdog.ps1 install-scheduled-task.ps1 install-watchdog-task.ps1 verify-system.ps1 .gitignore .gitattributes .github/workflows/daily-shelf.yml | Out-Null
    $status = git status --porcelain
    if ($status) {
        $stamp = Get-Date -Format 'yyyy-MM-dd'
        git commit -m "Daily shelf update $stamp" | Out-Null
        git push origin main | Out-Null
        Write-RunLog 'Committed and pushed site update.'
        try {
            & $python $indexNowPath --wait-for-key-seconds 90
            if ($LASTEXITCODE -eq 0) {
                Write-RunLog 'IndexNow submission complete.'
            }
            else {
                Write-RunLog "IndexNow submission returned exit code $LASTEXITCODE."
            }
        }
        catch {
            Write-RunLog "IndexNow submission failed: $($_.Exception.Message)"
        }
        try {
            & $python $calmSproutIndexNowPath --wait-for-key-seconds 90
            if ($LASTEXITCODE -eq 0) {
                Write-RunLog 'CalmSprout IndexNow submission complete.'
            }
            else {
                Write-RunLog "CalmSprout IndexNow submission returned exit code $LASTEXITCODE."
            }
        }
        catch {
            Write-RunLog "CalmSprout IndexNow submission failed: $($_.Exception.Message)"
        }
    }
    else {
        Write-RunLog 'No git changes to publish.'
    }
}
else {
    Write-RunLog 'No git repository found yet; generated files only.'
}

Write-RunLog 'Daily Autodigital Shelf run complete.'
