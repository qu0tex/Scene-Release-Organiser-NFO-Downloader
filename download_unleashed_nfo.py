import subprocess
import os
import sys
import ssl
import json
import time
import shutil
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

required_packages = [
    "webdriver-manager",
    "selenium",
    "urllib3",
    "json",
    "time",
    "colorama",
]

def install_missing_packages():
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"Package '{package}' not found. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_missing_packages()

webdriver_dir = r"C:\0day_and_eBook_Processing_Tool_v0.2_by_Quotex\WebDrivers"
os.makedirs(webdriver_dir, exist_ok=True)

driver = None

try:
    print("[*] Trying Chrome...")
    chrome_path = ChromeDriverManager().install()
    shutil.copy(chrome_path, os.path.join(webdriver_dir, "chromedriver.exe"))
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--silent")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_service = ChromeService(
        executable_path=os.path.join(webdriver_dir, "chromedriver.exe"),
        log_path=os.devnull
    )
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    print("[+] Chrome launched in headless mode.")
except Exception as chrome_error:
    print(f"[!] Chrome failed: {chrome_error}")
    try:
        print("[*] Trying Firefox...")
        gecko_path = GeckoDriverManager().install()
        shutil.copy(gecko_path, os.path.join(webdriver_dir, "geckodriver.exe"))
        
        firefox_options = FirefoxOptions()
        firefox_options.add_argument("--headless")

        driver = webdriver.Firefox(
            service=FirefoxService(os.path.join(webdriver_dir, "geckodriver.exe")),
            options=firefox_options
        )
        print("[+] Firefox launched in headless mode.")
    except Exception as firefox_error:
        print(f"[!] Firefox failed: {firefox_error}")
        print("[X] No supported browser could be started.")
        exit(1)

def try_download_from_srrdb_api(folder_name, nfo_path):
    try:
        context = ssl._create_unverified_context()
        url = f"https://api.srrdb.com/v1/nfo/{folder_name}"
        with urllib.request.urlopen(url, context=context) as response:
            if response.status != 200:
                print(f"SRRDB NFO API error for {folder_name}: HTTP {response.status}")
                return False
            data = json.loads(response.read().decode("utf-8"))
            if not data or "nfos" not in data or not data["nfos"]:
                print(f"No NFOs listed in SRRDB for {folder_name}")
                return False
            for nfo in data["nfos"]:
                if "url" in nfo:
                    urllib.request.urlretrieve(nfo["url"], nfo_path)
                    print(f"[+] Downloaded from SRRDB API: {nfo_path}")
                    return True
    except Exception as e:
        print(f"[!] SRRDB API lookup failed for {folder_name}: {e}")
    return False

def try_download_from_srrdb_web(folder_name, nfo_path):
    try:
        url = f"https://www.srrdb.com/download/file/{folder_name}/unleashed.nfo"
        urllib.request.urlretrieve(url, nfo_path)
        if os.path.exists(nfo_path) and os.path.getsize(nfo_path) > 0:
            print(f"[+] Downloaded from direct SRRDB link: {nfo_path}")
            return True
    except Exception as e:
        print(f"[!] Direct SRRDB link failed for {folder_name}: {e}")
    return False

def download_nfo(folder_path):
    folder_name = os.path.basename(folder_path)
    nfo_path = os.path.join(folder_path, 'unleashed.nfo')
    if os.path.exists(nfo_path):
        print(f"[-] Skipping {folder_name} - 'unleashed.nfo' already exists.")
        return
    if not os.path.isdir(folder_path):
        print(f"[!] Folder not found: {folder_path}")
        return
    if try_download_from_srrdb_api(folder_name, nfo_path):
        return
    if try_download_from_srrdb_web(folder_name, nfo_path):
        return
    url = f'https://predb.net/rls/{folder_name}'
    try:
        driver.get(url)
        print(f"[*] Opened {url} for {folder_name}")
        try:
            print(f"[*] Trying to find 'Download NFO' button for {folder_name}...")
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Download NFO')]"))
            )
            download_nfo_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Download NFO')]")
            download_url = download_nfo_button.get_attribute('href')
            urllib.request.urlretrieve(download_url, nfo_path)
            print(f"[+] Downloaded from predb.net: {nfo_path}")
        except Exception:
            print(f"[-] 'Download NFO' not found for {folder_name}, trying 'Show NFO'...")
            try:
                show_nfo_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Show NFO')]"))
                )
                show_nfo_button.click()
                time.sleep(2)
                download_nfo_button = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Download NFO')]"))
                )
                download_url = download_nfo_button.get_attribute('href')
                urllib.request.urlretrieve(download_url, nfo_path)
                print(f"[+] Downloaded after clicking 'Show NFO': {nfo_path}")
            except Exception:
                print(f"[X] No NFO available for {folder_name}. Skipping.\n")
    except Exception as e:
        print(f"[!] Error processing {folder_name}: {e}")

def check_for_unleashed_releases(base_path):
    for folder in os.listdir(base_path):
        full_folder_path = os.path.join(base_path, folder)
        if os.path.isdir(full_folder_path) and '-Unleashed' in folder:
            return True
    return False
if len(sys.argv) > 1:
    base_path = sys.argv[1]
else:
    from tkinter import Tk, filedialog
    root = Tk()
    root.withdraw()
    base_path = filedialog.askdirectory(title="Select folder containing Unleashed releases")
    if not base_path:
        print("[X] No folder selected. Exiting.")
        if driver:
            driver.quit()
        exit()

if not os.path.isdir(base_path):
    print("[ERROR] Folder does not exist. Try again.")
    input("Press Enter to continue...")
    if driver:
        driver.quit()
    exit()

if not check_for_unleashed_releases(base_path):
    print("[*] No '-Unleashed' releases found in the selected folder. Skipping NFO download.")
    if driver:
        driver.quit()
    exit()

for folder in os.listdir(base_path):
    full_folder_path = os.path.join(base_path, folder)
    if os.path.isdir(full_folder_path) and '-Unleashed' in folder:
        print(f"\n=== Processing folder: {folder} ===")
        download_nfo(full_folder_path)

if driver:
    driver.quit()
    print("[*] Browser closed.")

print("\n[DONE] Processing complete.")
