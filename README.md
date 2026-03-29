# 🛠️ Custom DNS Server

## 📌 Overview
A lightweight **DNS server** built in Python using [dnslib](https://pypi.org/project/dnslib/).
It supports local zone resolution, recursive forwarding, caching, and structured logging for analysis.
Designed for hands‑on exploration of DNS internals, performance testing, and educational demos.

---

## ⚙️ Features
- UDP request handling
- DNS header parsing via `dnslib`
- Local zone resolution (example.local)
- Recursive forwarding to **Google DNS (8.8.8.8)**
- Thread‑safe upstream response caching into `ZONE`
- Plain file logging (`dns.log`) with CSV conversion via `logtocsv.py`
- Concurrent performance benchmarking with `perf_test.py`

---

## 🗂️ File Structure
Custom-DNS-Server/
│── dns_server.py
│── logtocsv.py
│── perf_test.py
│── LICENSE
│── README.md

---

## ⚙️ Installation
Clone the repository and install dependencies:

```bash
git clone https://github.com/Boffin-Omega/Custom-DNS-Server.git
cd Custom-DNS-Server
pip install dnslib
---

## 🚀 Usage

### Start the DNS Server
```bash
python dns_server.py
Default host: 127.0.0.1
Default port: 5053

---

### Convert Logs to CSV
```bash
python logtocsv.py

---

### Run Performance Tests
```bash
python perf_test.py

---

## 🧩 Tech Stack
- **Language:** Python 3.x
- **Library:** dnslib
- **Networking:** UDP sockets
- **Data Handling:** CSV log conversion
- **Testing:** Multithreaded performance benchmarking
