Scene Release Organiser - 0day and eBook Processing Tool v0.2 by Quotex

This tool is a Windows batch/python script designed to automate the extraction, sorting, and clean-up of Scene releases, especially for 0day and eBook packs plus more!
_____________________________________________________________________________________
✅ v0.2 Updates =

- Reworked the script and made things cleaner and easier to use.
- You can now choose any folder to process instead of moving the script each time. (e.g., TL-0day-XX, TL-0day-EBOOKS-XX).
- Added manual .nfo download mode — simply enter one or more release names.
- Now uses https://srrdb.com as the main NFO source, with https://predb.net as a fallback.
- Reworked the menu to include all possible task combinations (1 through 15).
- Added the ability to run another task directly after the current one finishes, removing the need to restart the script.
- Fixed a bug that incorrectly moved non-gamerip releases to _gamerips. (such as rGPDA etc.)
- Improved logging: now only shows actual errors in ProcessErrorLog.txt.
- Coloured console output for improved readability.
_____________________________________________________________________________________
✨ Features =

- Extracts missing file_id.diz from .zip archives using 7-Zip. (fallbacks to WinRAR if 7-Zip is not installed.).
- Moves foreign-language releases based on folder name keywords like GERMAN, FRENCH, SPANISH, etc to a _foreign folder. 
- Moves broken releases that have corrupted or invalid archives to a _bad folder.
- Moves known gamerip releases (from -Unleashed, -RAZOR, -VACE, etc.) to a _gamerips folder.
- Downloads missing .nfo files for Unleashed releases. (only .diz is included in their archives).
- Download any .nfo file for one or more releases by entering space-separated release names.
- Optional logging — a ProcessErrorLog.txt is only created if issues are detected.
_____________________________________________________________________________________
🔧 Requirements =

### Software :

- [7-Zip] - (https://7-zip.org) - Required to extract ".diz" files.
- [WinRAR] - (https://win-rar.com) - Used as a fallback for ".diz" extraction.
- [Python 3.13.3] - (https://python.org/downloads/release/python-3133/) - Required for everything to work.
- Python Packages: [Selenium] - (https://selenium.dev/downloads/)
                   [Colorama] - (https://github.com/tartley/colorama)
- Install via terminal: "pip install selenium" + "pip install colorama" (e.g C:\Python313\python.exe -m pip install colorama)

### WebDriver : (for NFO downloading.)

- [GeckoDriver (Firefox)] - (https://github.com/mozilla/geckodriver/releases)
- [ChromeDriver (Chrome)] - (https://developer.chrome.com/docs/chromedriver/downloads)

📂 If manually downloading place the WebDriver executables in: C:\0day_and_eBook_Processing_Too_v0.2_by_Quotex\WebDrivers\
   (Or adjust the path in the Python scripts.)
_____________________________________________________________________________________
▶️ How to Use =

1. Download "0day_and_eBook_Processing_Tool_v0.2_by_Quotex-TL.zip" from TL forums. (CRC: f409ab46)
2. Extract the folder "0day_and_eBook_Processing_Too_v0.2_by_Quotex" to:
   - C:\0day_and_eBook_Processing_Too_v0.2_by_Quotex
   - (If you extract it elsewhere, you’ll need to manually edit the script paths.)
3. Double-click the .bat or .ps1 (Powershell version) file to launch the menu.
   - Paste or drag a folder (e.g., TL-0day-XX) when prompted.
4. Choose a task (1–15) from the menu:
   - Option 1: Full process — extract .diz, move foreign releases, download Unleashed .nfos and move gamerips.
   - Other options allow for more granular control.
5. Any errors (e.g., corrupt archives, missing files or failed .nfo downloads) will be saved in ProcessErrorLog.txt.
_____________________________________________________________________________________
🔍 Notes =

- The script auto-selects Firefox for Selenium if available, otherwise it falls back to Chrome if Firefox is not installed.
- During .nfo downloading, a browser window may briefly open — do not close it manually, it will close on its own when finished.
- The tool is designed with Scene standards in mind, ensuring your folders stay clean and properly organized.
_____________________________________________________________________________________
🛠️ Created by Quotex for TL

If you encounter issues or have feature suggestions, feel free to reach out. Thanks for using! 🙂