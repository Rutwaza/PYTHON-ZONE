import requests
import time


# Clean proxies by removing extra information after IP:Port and handling empty lines
def clean_proxies(proxies):
    cleaned_proxies = []
    for proxy in proxies:
        if proxy.strip():  # Ensure we skip empty lines
            try:
                proxy = proxy.split()[0]  # Take only the IP:Port part
                if ':' in proxy:
                    cleaned_proxies.append(proxy)
            except IndexError:
                continue  # Skip lines that don't have a valid format
    return cleaned_proxies


def fetch_proxies(api_urls, retries=3, delay=5):
    print("Fetching proxies...")
    all_proxies = []

    for api_url in api_urls:
        print(f"Trying to fetch proxies from {api_url}")
        for _ in range(retries):
            try:
                response = requests.get(api_url)
                response.raise_for_status()

                # Check if the response is JSON or plain text
                if "application/json" in response.headers.get("Content-Type", ""):
                    proxy_list = response.json().get('data', [])
                    proxies = [f"{proxy['ip']}:{proxy['port']}" for proxy in proxy_list]
                else:
                    # Assume it's plain text (like spys.me) and clean the proxies
                    proxies = clean_proxies(response.text.splitlines())

                if proxies:
                    print(f"[SUCCESS] Proxies fetched successfully from {api_url}")
                    all_proxies.extend(proxies)
                    break  # Break after successful fetch
            except requests.RequestException as e:
                print(f"[FAILED] Error fetching proxies from {api_url}: {e}")
                time.sleep(delay)
            except ValueError as e:
                print(f"[FAILED] Error parsing response from {api_url}: {e}")

    return all_proxies


def load_existing_proxies(file_path='proxies.txt'):
    try:
        with open(file_path, 'r') as file:
            # Read existing proxies, removing duplicates
            return set(file.read().splitlines())
    except FileNotFoundError:
        return set()  # Return an empty set if the file doesn't exist


def save_proxies_to_file(proxies, file_path='proxies.txt'):
    # Load existing proxies to avoid duplicates
    existing_proxies = load_existing_proxies(file_path)

    # Remove any proxies that already exist in the file
    new_proxies = set(proxies) - existing_proxies

    if new_proxies:
        with open(file_path, 'a') as file:  # Open in append mode ('a')
            for proxy in new_proxies:
                file.write(f"{proxy}\n")
        print(f"[SUCCESS] {len(new_proxies)} new proxies appended to {file_path}")
    else:
        print(f"[INFO] No new proxies to append. All fetched proxies already exist.")


def main():
    # List of proxy API URLs
    proxy_api_urls = [
        "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc",
        "https://www.proxy-list.download/api/v1/get?type=https",
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=1000&country=all&ssl=all&anonymity=all",
        "https://spys.me/proxy.txt",
        "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt",  # Proxy list in text format
        "https://www.sslproxies.org",  # Free SSL proxies
        "https://www.us-proxy.org",  # US proxy
        "https://www.socks-proxy.net",  # SOCKS proxies
        "https://www.free-proxy-list.net/uk-proxy.html",  # UK proxy list
        "https://www.freeproxylists.net/?c=US"  # Free proxy list for US
    ]

    # Fetch proxies
    proxies = fetch_proxies(proxy_api_urls)

    # Save proxies to file (without duplicates)
    if proxies:
        save_proxies_to_file(proxies, 'proxies.txt')
    else:
        print("[ERROR] No proxies fetched.")


if __name__ == "__main__":
    main()
