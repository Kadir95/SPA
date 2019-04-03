import socket

def get_host_ip():
    hostname = socket.gethostname()    
    ip_addr = socket.gethostbyname(hostname)
    return ip_addr