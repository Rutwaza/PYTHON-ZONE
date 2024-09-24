# Open the input file containing proxies (one per line)
with open("newprox.txt", "r") as infile:
    # Open the output file to save the formatted proxies
    with open("proxies2.txt", "w") as outfile:
        # Read each line (proxy) from the input file
        for line in infile:
            # Remove 'http://' or 'socks4://' from the start of each proxy and strip any extra whitespace
            formatted_proxy = line.replace("http://", "").replace("socks4://", "").strip()
            # Write the formatted proxy to the output file
            outfile.write(formatted_proxy + "\n")

print("Formatted proxies saved to proxies2.txt")
