🛠️ Custom DNS Server

📌 Overview
A lightweight DNS server built in Python using dnslib.
It supports local zone resolution, recursive forwarding, caching, and structured logging for analysis.

This project is designed for:
-Hands-on exploration of DNS internals
-Performance testing
-Educational demonstrations


⚙️ Features

✅ UDP request handling
✅ DNS header parsing via dnslib
✅ Local zone resolution (example.local)
✅ Recursive forwarding to Google DNS (8.8.8.8)
✅ Thread-safe upstream response caching into ZONE
✅ Plain file logging (dns.log)
✅ CSV conversion via logtocsv.py
✅ Concurrent performance benchmarking with perf_test.py


🗂️ File Structure

Custom-DNS-Server/
├── dns_server.py
├── logtocsv.py
├── perf_test.py
├── LICENSE
└── README.md


⚙️ Installation

Clone the repository and install dependencies:

git clone https://github.com/Boffin-Omega/Custom-DNS-Server.git
cd Custom-DNS-Server
pip install dnslib


🚀 Usage

1-> ▶️ Start the DNS Server -> python dns_server.py

-Default Configuration:
    Host: 127.0.0.1
    Port: 5053

2-> 📊 Convert Logs to CSV -> python logtocsv.py

3-> ⚡ Run Performance Tests -> python perf_test.py


🧩 Tech Stack

Language: Python 3.x
Library: dnslib
Networking: UDP sockets
Data Handling: CSV log conversion
Testing: Multithreaded performance benchmarking