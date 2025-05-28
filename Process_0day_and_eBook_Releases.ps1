$toolPath = "C:\0day_and_eBook_Processing_Tool_v0.2_by_Quotex"
$pythonPath = "C:\Python313\python.exe"
$scriptPath = "$toolPath\Scripts\main.py"

function Show-Menu {
    Clear-Host
    Write-Host "0day and eBook Processing Tool v0.2 by Quotex for TL`n" -ForegroundColor Cyan
    Write-Host "[ 1] Extract file_id.diz + Move foreign releases + Download Unleashed NFOs" -ForegroundColor Yellow
    Write-Host "[ 2] Extract file_id.diz + Move foreign releases + Move 0day Gamerips" -ForegroundColor Yellow
    Write-Host "[ 3] Extract file_id.diz + Move foreign releases + Download Unleashed NFOs + Move 0day Gamerips" -ForegroundColor Yellow
    Write-Host "[ 4] Extract file_id.diz + Move foreign releases" -ForegroundColor Yellow
    Write-Host "[ 5] Extract file_id.diz + Download Unleashed NFOs + Move 0day Gamerips" -ForegroundColor Yellow
    Write-Host "[ 6] Extract file_id.diz + Download Unleashed NFOs" -ForegroundColor Yellow
    Write-Host "[ 7] Extract file_id.diz + Move 0day Gamerips" -ForegroundColor Yellow
    Write-Host "[ 8] Extract file_id.diz only" -ForegroundColor Yellow
    Write-Host "[ 9] Move foreign releases + Download Unleashed NFOs" -ForegroundColor Yellow
    Write-Host "[10] Move foreign releases + Download Unleashed NFOs + Move 0day Gamerips" -ForegroundColor Yellow
    Write-Host "[11] Move foreign releases only (to _foreign)" -ForegroundColor Yellow
    Write-Host "[12] Move 0day Gamerips + Download Unleashed NFOs" -ForegroundColor Yellow
    Write-Host "[13] Move 0day Gamerips only (to _gamerips)" -ForegroundColor Yellow
    Write-Host "[14] Download Unleashed NFOs only" -ForegroundColor Yellow
    Write-Host "[15] NFO Downloader (Enter any release name to download the .nfo)" -ForegroundColor Yellow
}

function Get-Args {
    param ($choice)

    switch ($choice) {
        1  { return "--extract --moveforeign --unleashed" }
        2  { return "--extract --moveforeign --gamerips" }
        3  { return "--extract --moveforeign --unleashed --gamerips" }
        4  { return "--extract --moveforeign" }
        5  { return "--extract --unleashed --gamerips" }
        6  { return "--extract --unleashed" }
        7  { return "--extract --gamerips" }
        8  { return "--extract" }
        9  { return "--moveforeign --unleashed" }
        10 { return "--moveforeign --unleashed --gamerips" }
        11 { return "--moveforeign" }
        12 { return "--gamerips --unleashed" }
        13 { return "--gamerips" }
        14 { return "--unleashed" }
        default { return "" }
    }
}

do {
    Show-Menu
    $target = Read-Host "`nEnter the full path of the folder you want to process (or drag it here)"
    
    if (-not (Test-Path $target)) {
        Write-Host "`n[ERROR] Folder does not exist. Try again." -ForegroundColor Red
        Pause
        continue
    }

    $choice = Read-Host "`nSelect an option (1-15)"
    
    if ($choice -eq "15") {
        $rel = Read-Host "`nEnter one or more release names to download .nfo (space-separated):"
        Write-Host "[INFO] Downloading NFO for releases: $rel" -ForegroundColor Cyan
        & $pythonPath "$toolPath\Scripts\nfo_downloader.py" "$rel"
    } else {
        $args = Get-Args $choice
        if ($args -eq "") {
            Write-Host "`n[ERROR] Invalid selection. Try again." -ForegroundColor Red
            Pause
            continue
        }
        Write-Host "[INFO] Running with arguments: $args" -ForegroundColor Cyan
        & $pythonPath $scriptPath --path "$target" @($args -split ' ')
    }

    $again = Read-Host "`nWould you like to choose another option? (Y/N)"
} while ($again -match "^(Y|y)$")

Write-Host "`nExiting. Thank you." -ForegroundColor Green
Start-Sleep -Seconds 2
