import requests
import time
import signal
import sys
from colorama import Fore, Style, init
import os

# Initialize colorama
init(autoreset=True)

# Global flag to track if the user interrupted the test
interrupted = False
progress_file = 'progress.txt'  # File to store the progress

# Signal handler for user interruption (Ctrl+C)
def signal_handler(sig, frame):
    global interrupted
    print(Fore.YELLOW + "\n[INFO] Test interrupted by user.")
    interrupted = True

# Function to test a single proxy
def verify_proxy(proxy, test_url='http://httpbin.org/ip', timeout=5):
    proxies = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}',
    }
    try:
        response = requests.get(test_url, proxies=proxies, timeout=timeout)
        if response.status_code == 200:
            print(Fore.GREEN + f"[SUCCESS] Proxy {proxy} is working. Response: {response.text.strip()}")
            return True
    except requests.RequestException:
        print(Fore.RED + f"[FAILED] Proxy {proxy} failed.")
    return False

# Function to load existing working proxies from file to avoid duplication
def load_existing_working_proxies(file_path='working_proxies.txt'):
    try:
        with open(file_path, 'r') as file:
            return set(line.strip() for line in file)
    except FileNotFoundError:
        return set()

# Function to save the current progress (last tested proxy index)
def save_progress(index):
    with open(progress_file, 'w') as file:
        file.write(str(index))

# Function to load progress from the progress file
def load_progress():
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as file:
            return int(file.read().strip())
    return 0  # Start from the beginning if no progress file exists

# Function to verify a list of proxies and save non-duplicates to a file
def verify_proxies(proxy_list, output_file='working_proxies.txt', timeout=5):
    working_proxies = []
    existing_proxies = load_existing_working_proxies(output_file)  # Load existing working proxies
    start_index = load_progress()  # Load progress from the last run

    try:
        for index, proxy in enumerate(proxy_list[start_index:], start=start_index + 1):  # Start from last tested proxy
            if interrupted:
                save_progress(index - 1)  # Save progress when interrupted
                break

            print(f"[INFO] Testing proxy {index}/{len(proxy_list)}: {proxy}")
            if proxy not in existing_proxies and verify_proxy(proxy, timeout=timeout):
                working_proxies.append(proxy)
                time.sleep(0.5)  # Adding a short delay between tests

    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n[INFO] Test interrupted by user.")
        save_progress(index)  # Save progress on interruption

    # Save the new working proxies to the file
    if working_proxies:
        with open(output_file, 'a') as file:  # Append mode to add new working proxies
            for proxy in working_proxies:
                file.write(f"{proxy}\n")
        print(Fore.GREEN + f"[INFO] {len(working_proxies)} new working proxies appended to {output_file}.")
    else:
        print(Fore.YELLOW + "[INFO] No new working proxies found or all proxies already exist.")

# Function to load proxies from a file
def load_proxies_from_file(file_path='proxies2.txt'):
    with open(file_path, 'r') as file:
        proxies = [line.strip() for line in file.readlines()]
    return proxies

def main():
    signal.signal(signal.SIGINT, signal_handler)  # Register the signal handler for Ctrl+C
    proxy_file = 'proxies2.txt'
    test_url = 'http://httpbin.org/ip'  # Test URL to verify the proxies

    # Load proxies from file
    proxies = load_proxies_from_file(proxy_file)

    if proxies:
        print(f"[INFO] Verifying {len(proxies)} proxies...")
        verify_proxies(proxies, output_file='working_proxies.txt', timeout=10)
    else:
        print(Fore.RED + "[ERROR] No proxies loaded from file.")

if __name__ == "__main__":
    main()
