import csv

FIELDS = ["timestamp", "qname", "qtype", "addr", "resolution_method", "response_time_ms"]

with open("dns.log") as f, open("dns.csv", "w", newline="") as out:
    writer = csv.writer(out)
    writer.writerow(FIELDS)
    for line in f:
        line = line.strip()
        if line:
            writer.writerow(line.split(",", maxsplit=5))
print("done → dns.csv")