sockFlood V1.0
"Disclaimer: This tool is for educational and testing purposes only. The author is not responsible for any damage caused by misuse of this tool."

Overview
sockFlood is a powerful tool for network stress testing and Denial of Service (DoS) attacks. It can flood a target with a large number of UDP packets, overwhelming its network bandwidth and causing it to crash or become unresponsive.

Features
Flood a target with UDP packets
Customize the number of attack threads
Supports both websites and IP addresses as targets
Installation
Clone the repository: git clone https://github.com/markbty24/sockFlood.git
Navigate to the sockFlood directory: cd sockFlood
Install the required dependencies: pip install -r requirements.txt
Run the program: python sockFlood.py
Usage
Enter the website or IP address you want to attack when prompted.
If attacking a website, ensure that the address is correct and that the website is not protected by a Distributed Denial of Service (DDoS) protection service.
Customize the number of attack threads if desired. The default value is 1000.
Start the attack by typing start and pressing Enter.
Example Usage
``MR-infinity >> attack
Enter the website or IP address to attack : example.com

MR-infinity >> amount
Enter the number of threads [default = 1000]: 5000

MR-infinity >> start
[+] Started flooding example.com with 5000 threads!``

Warning
Use this tool at your own risk. It is intended for educational and testing purposes only. Any damage caused by the misuse of this tool is the responsibility of the user.

Follow me on Instagram
For more programming tips and tutorials, follow me on Instagram.

License
This tool is released under the MIT License.



