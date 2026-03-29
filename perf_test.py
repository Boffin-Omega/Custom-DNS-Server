"""
Concurrent DNS performance tester
Sends queries in parallel and reports QPS and success rate.
Run against the server in both THREADED=True and THREADED=False to compare.
"""

import socket
import struct
import threading
import time
import random
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

SERVER = ("127.0.0.1", 5053)
NAMES = [
    "example.local.", "mail.example.local.", "www.example.local.",  # local zone
    "google.com.", "github.com.", "cloudflare.com.", "amazon.com.",  # external
    "wikipedia.org.", "stackoverflow.com.", "youtube.com.",          # external
]

success_count = 0
lock = threading.Lock()

def build_query(name):
    txid = random.randint(0, 0xFFFF)
    header = struct.pack(">HHHHHH", txid, 0x0100, 1, 0, 0, 0)
    qname = b"".join(bytes([len(l)]) + l.encode() for l in name.rstrip(".").split(".")) + b"\x00"
    return header + qname + struct.pack(">HH", 1, 1)

def query():
    global success_count

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(3)
    try:
        sock.sendto(build_query(random.choice(NAMES)), SERVER)
        sock.recvfrom(512)
        #only one thread should be able to modify success count
        with lock:
            success_count += 1
            logging.info("DNS query completed successfuly")

    except Exception as e:
        logging.error(f"Exception occured: {e}")
    finally:
        sock.close()

def run(total=200, concurrency=20):
    threads = [threading.Thread(target=query) for _ in range(total)]

    start = time.time()
    for i in range(0, total, concurrency):
        batch = threads[i:i+concurrency]
        for t in batch: t.start()
        for t in batch: t.join()
    elapsed = time.time() - start

    print(f"\n{total} queries in {elapsed:.2f}s  |  {total/elapsed:.0f} QPS  |  {success_count}/{total} successful\n")

if __name__ == "__main__":
    run()