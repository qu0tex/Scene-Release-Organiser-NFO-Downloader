import subprocess
import sys
import os
import json
import urllib.request
import ssl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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

def try_download_from_srrdb_api(folder_name, nfo_path):
    try:
        context = ssl._create_unverified_context()
        url = f"https://api.srrdb.com/v1/nfo/{folder_name}"
        with urllib.request.urlopen(url, context=context) as response:
            content = response.read()
        nfo_data = json.loads(content.decode('utf-8'))
        if 'nfolink' in nfo_data and len(nfo_data['nfolink']) > 0:
            nfo_file_name = nfo_data['nfo'][0]
            nfo_url = nfo_data['nfolink'][0]
            nfo_path = os.path.join(os.path.dirname(nfo_path), nfo_file_name)
            urllib.request.urlretrieve(nfo_url, nfo_path)
            print(f"Downloaded from SRRDB API: {nfo_path}")
            return True
        else:
            print(f"No valid NFO link found for {folder_name} via SRRDB API")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"NFO not found via SRRDB API for {folder_name}")
        else:
            print(f"SRRDB API error for {folder_name}: HTTP {e.code}")
    except Exception as e:
        print(f"SRRDB API lookup failed for {folder_name}: {e}")
    return False

def try_download_from_srrdb_web(folder_name, nfo_path):
    try:
        context = ssl._create_unverified_context()
        url = f"https://www.srrdb.com/download/file/{folder_name}/"
        urllib.request.urlretrieve(url, nfo_path)
        if os.path.exists(nfo_path):
            print(f"Downloaded from direct link: {nfo_path}")
            return True
    except Exception as e:
        print(f"Direct SRRDB link failed for {folder_name}: {e}")
    return False

def download_nfo(folder_name):
    folder_path = os.path.join(os.getcwd(), folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created folder: {folder_path}")
    nfo_path = os.path.join(folder_path, f'{folder_name}.nfo')
    if os.path.exists(nfo_path):
        print(f"Skipping {folder_name} - '{folder_name}.nfo' already exists.")
        return
    if not os.path.isdir(folder_path):
        print(f"Folder not found: {folder_path}")
        return
    if try_download_from_srrdb_api(folder_name, nfo_path):
        return
    if try_download_from_srrdb_web(folder_name, nfo_path):
        return
    url = f'https://predb.net/rls/{folder_name}'
    driver.get(url)
    
    try:
        print(f"Trying to find 'Download NFO' button for {folder_name}...")
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Download NFO')]"))
        )
        download_nfo_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Download NFO')]")
        download_url = download_nfo_button.get_attribute('href')
        urllib.request.urlretrieve(download_url, nfo_path)
        print(f"Downloaded and saved as: {nfo_path}")
    except Exception:
        print(f"'Download NFO' not found for {folder_name}. Trying to click 'Show NFO'...")
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
            print(f"Downloaded and saved as: {nfo_path}")
        except Exception:
            print(f"No NFO available for {folder_name}. Skipping.\n")
            return

if __name__ == '__main__':
    release_name = input("Enter full release name (e.g., Title.Name.2025-GRP): ").strip()
    print(f"Attempting to download .nfo for: {release_name}")
    download_nfo(release_name)
