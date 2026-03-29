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

---

## 📄 License

MIT License

Copyright (c) 2026 C.K Gagan Gowda

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
