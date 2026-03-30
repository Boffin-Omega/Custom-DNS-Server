"""
Lightweight DNS Server using dnslib
- UDP request handling
- DNS header parsing (via dnslib)
- Local zone resolution
- Recursive forwarding to 8.8.8.8
- Upstream response caching into ZONE (thread-safe)
- Plain file logging, converted to CSV via log_to_csv.py
"""
import socket
import threading
import logging
import time
from dnslib import DNSRecord, RR, QTYPE, RCODE
import dnslib

HOST     = "127.0.0.1"
PORT     = 5053
UPSTREAM = ("8.8.8.8", 53)
THREADED = False
LOG_FILE = "dns.log"

ZONE_FILE = """
example.local.      300  IN  A     192.168.1.10
mail.example.local. 300  IN  A     192.168.1.20
www.example.local.  300  IN  CNAME example.local.
"""

'''
{
    (example.local., A):[example.local., 300,IN,A,192.168.1.10]
]
}
'''
ZONE      = {}
ZONE_LOCK = threading.Lock()

for rr in RR.fromZone(ZONE_FILE):
    key = (str(rr.rname).lower(), rr.rtype)
    ZONE.setdefault(key, []).append(rr)

_static_keys = set(ZONE.keys())

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.FileHandler(LOG_FILE, mode="w"), logging.StreamHandler()]
)

def log_query(resolution_method, qname, qtype, addr, response_time_ms=0):
    msg = f"{time.strftime('%Y-%m-%d %H:%M:%S')},{qname},{qtype},{addr[0]}:{addr[1]},{resolution_method},{round(response_time_ms, 2)}"
    logging.info(msg)
    print(f"  [{resolution_method.upper():>10}]  {qname}  {qtype}  from {addr[0]}:{addr[1]}  {response_time_ms:.1f}ms")

def zone_get(qname, qtype):
    with ZONE_LOCK:
        return list(ZONE.get((qname, qtype), []))

def zone_cache(rr_list):
    with ZONE_LOCK:
        for rr in rr_list:
            key = (str(rr.rname).lower(), rr.rtype)
            if key not in ZONE:
                ZONE[key] = [rr]
            else:
                seen = {str(x.rdata) for x in ZONE[key]}
                if str(rr.rdata) not in seen:
                    ZONE[key].append(rr)

def is_static_zone_key(qname, qtype):
    return (qname, qtype) in _static_keys


def handle(data, addr, sock):
    try:
        request = DNSRecord.parse(data)
    except dnslib.DNSError:
        log_query("error", "<malformed>", "?", addr)
        return

    q     = request.questions[0]
    qname = str(q.qname).lower()
    qtype = QTYPE.get(q.qtype)

    if len(qname) > 255 or ".." in qname:
        reply = request.reply()
        reply.header.rcode = RCODE.FORMERR
        sock.sendto(reply.pack(), addr)
        log_query("error", qname, qtype, addr)
        return

    answers = zone_get(qname, q.qtype)
    if answers:
        reply = request.reply()
        for rr in answers:
            reply.add_answer(rr)
        sock.sendto(reply.pack(), addr)
        outcome = "zone" if is_static_zone_key(qname, q.qtype) else "cached"
        log_query(outcome, qname, qtype, addr)
        return

    usock = None
    t0 = time.perf_counter()
    try:
        usock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        usock.settimeout(3)
        usock.sendto(data, UPSTREAM)
        response, _ = usock.recvfrom(512)
    except (OSError, TimeoutError) as e:
        elapsed = (time.perf_counter() - t0) * 1000
        reply = request.reply()
        reply.header.rcode = RCODE.SERVFAIL
        sock.sendto(reply.pack(), addr)
        log_query("error", qname, qtype, addr, response_time_ms=elapsed)
        return
    finally:
        if usock:
            usock.close()

    elapsed = (time.perf_counter() - t0) * 1000
    try:
        response_record = DNSRecord.parse(response)
    except dnslib.DNSError:
        log_query("error", qname, qtype, addr, response_time_ms=elapsed)
        return
    
    sock.sendto(response, addr)
    zone_cache(response_record.rr)
    log_query("forwarded", qname, qtype, addr,  response_time_ms=elapsed)

def run():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1.0)
    sock.bind((HOST, PORT))
    print(f"DNS server running on {HOST}:{PORT} ({'threaded' if THREADED else 'single-threaded'})")
    print(f"Logging to {LOG_FILE}\n")
    try:
        while True:
            try:
                data, addr = sock.recvfrom(512)
            except socket.timeout:
                continue
            if THREADED:
                threading.Thread(target=handle, args=(data, addr, sock), daemon=True).start()
            else:
                handle(data, addr, sock)
    except KeyboardInterrupt:
        print("\nShutting down")
    finally:
        sock.close()

if __name__ == "__main__":
    run()