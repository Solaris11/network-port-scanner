import socket
import signal
from ipaddress import ip_network

# Define the global timeout handler
def timeout_handler(signum, frame):
    raise TimeoutError

# Assign the handler for the signal
signal.signal(signal.SIGALRM, timeout_handler)

def is_port_open(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            return result == 0
    except socket.error:
        return False

def scan_ip(ip):
    print(f"Scanning IP: {ip}")
    open_ports = []
    for port in range(1, 1025):
        if is_port_open(ip, port):
            open_ports.append(port)
    return open_ports

def scan_range(ip_range):
    for ip in ip_network(ip_range):
        signal.alarm(10)  # Set the alarm for 10 seconds
        try:
            open_ports = scan_ip(str(ip))
            signal.alarm(0)  # Disable the alarm
            if open_ports:
                print(f"{ip}: Open ports: {open_ports}")
        except TimeoutError:
            print(f"{ip}: address timeout")
            signal.alarm(0)  # Disable the alarm

# Example usage:
# Replace '192.168.1.0/24' with the IP address or range you want to scan.
scan_range('192.168.1.0/24')