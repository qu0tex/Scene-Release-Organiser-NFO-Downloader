@echo off
title 0day and eBook Processing Tool v0.2 by Quotex for TL
cd /d "C:\0day_and_eBook_Processing_Tool_v0.2_by_Quotex"

for /f %%a in ('echo prompt $E^| cmd') do set "ESC=%%a"
set "RED=%ESC%[91m"
set "GREEN=%ESC%[92m"
set "YELLOW=%ESC%[93m"
set "CYAN=%ESC%[96m"
set "RESET=%ESC%[0m"

:ask_folder
cls
echo %CYAN%0day and eBook Processing Tool v0.2%RESET% by Quotex for %GREEN%TL%RESET%
echo.
set /p "target=Enter the full path of the folder you want to process (or drag it here): "
if not exist "%target%" (
    echo.
    echo %RED%[ERROR]%RESET% Folder does not exist. Try again.
    pause
    goto ask_folder
)

:menu
cls
echo %GREEN%+----------------------------------------------------------------------------+
echo ^|                 0day and eBook Processing Tool v0.2                        ^|
echo ^|                            by Quotex for TL                                ^|
echo +----------------------------------------------------------------------------+%RESET%
echo.
echo %CYAN%[ 1 ]%RESET%  Extract file_id.diz + Move foreign releases + Download Unleashed NFOs
echo %CYAN%[ 2 ]%RESET%  Extract file_id.diz + Move foreign releases + Move 0day Gamerips
echo %CYAN%[ 3 ]%RESET%  Extract file_id.diz + Move foreign releases + Download Unleashed NFOs + Move 0day Gamerips
echo %CYAN%[ 4 ]%RESET%  Extract file_id.diz + Move foreign releases
echo %CYAN%[ 5 ]%RESET%  Extract file_id.diz + Download Unleashed NFOs + Move 0day Gamerips
echo %CYAN%[ 6 ]%RESET%  Extract file_id.diz + Download Unleashed NFOs
echo %CYAN%[ 7 ]%RESET%  Extract file_id.diz + Move 0day Gamerips
echo %CYAN%[ 8 ]%RESET%  Extract file_id.diz only
echo %CYAN%[ 9 ]%RESET%  Move foreign releases + Download Unleashed NFOs
echo %CYAN%[10 ]%RESET%  Move foreign releases + Download Unleashed NFOs + Move 0day Gamerips
echo %CYAN%[11 ]%RESET%  Move foreign releases only (to _foreign)
echo %CYAN%[12 ]%RESET%  Move 0day Gamerips + Download Unleashed NFOs
echo %CYAN%[13 ]%RESET%  Move 0day Gamerips only (to _gamerips)
echo %CYAN%[14 ]%RESET%  Download Unleashed NFOs only
echo %CYAN%[15 ]%RESET%  NFO Downloader (Enter any release name it will download the .nfo)
echo.
set /p "choice=Select an option (1-15): "

set "args="
if "%choice%"=="1"  set args=--extract --moveforeign --unleashed
if "%choice%"=="2"  set args=--extract --moveforeign --gamerips
if "%choice%"=="3"  set args=--extract --moveforeign --unleashed --gamerips
if "%choice%"=="4"  set args=--extract --moveforeign
if "%choice%"=="5"  set args=--extract --unleashed --gamerips
if "%choice%"=="6"  set args=--extract --unleashed
if "%choice%"=="7"  set args=--extract --gamerips
if "%choice%"=="8"  set args=--extract
if "%choice%"=="9"  set args=--moveforeign --unleashed
if "%choice%"=="10" set args=--moveforeign --unleashed --gamerips
if "%choice%"=="11" set args=--moveforeign
if "%choice%"=="12" set args=--gamerips --unleashed
if "%choice%"=="13" set args=--gamerips
if "%choice%"=="14" set args=--unleashed
if "%choice%"=="15" (
    cls
    set /p "rel=Enter one or more release names to download .nfo (space-separated): "
    C:\Python313\python.exe Scripts\nfo_downloader.py %rel%
    goto continue
)

if "%args%"=="" (
    echo.
    echo %RED%[ERROR]%RESET% Invalid selection. Try again.
    pause
    goto menu
)

C:\Python313\python.exe Scripts\main.py --path "%target%" %args%

:continue
echo.
set /p "again=Would you like to choose another option? (%GREEN%Y%RESET%/%RED%N%RESET%): "
if /I "%again%"=="Y" goto ask_folder

echo.
echo %CYAN%Exiting.%RESET% Thank you.
timeout /t 2 >nul
exit

