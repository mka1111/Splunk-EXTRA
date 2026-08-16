import logging
import logging.handlers
import random
import time

# Map of facility name to SysLogHandler facility constant
FACILITIES = {
    "squid": logging.handlers.SysLogHandler.LOG_LOCAL1,
    "postfix": logging.handlers.SysLogHandler.LOG_LOCAL2,
    "cups": logging.handlers.SysLogHandler.LOG_LOCAL3,
}

SYSLOG_ADDRESS = "/dev/log"  # local syslog socket on Linux

def build_logger(name, facility):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.handlers.SysLogHandler(address=SYSLOG_ADDRESS, facility=facility)
    formatter = logging.Formatter(f"{name}: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

loggers = {name: build_logger(name, fac) for name, fac in FACILITIES.items()}

def random_ip():
    return f"{random.randint(10,192)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"

def random_user():
    return random.choice(["jdoe", "asmith", "mgarcia", "klee", "rpatel", "guest", "admin", "printer_svc"])

# --- Squid access-log style entries ---
squid_methods = ["GET", "POST", "CONNECT", "HEAD"]
squid_domains = ["example.com", "updates.microsoft.com", "cdn.cloudflare.com",
                  "mail.google.com", "s3.amazonaws.com", "ads.doubleclick.net"]
squid_codes = ["TCP_MISS/200", "TCP_HIT/200", "TCP_DENIED/403", "TCP_MISS/304", "TCP_MISS/502"]

def gen_squid_log():
    ts = f"{random.randint(1700000000,1750000000)}.{random.randint(100,999)}"
    elapsed = random.randint(1, 900)
    client = random_ip()
    code = random.choice(squid_codes)
    size = random.randint(200, 50000)
    method = random.choice(squid_methods)
    url = f"http://{random.choice(squid_domains)}/"
    user = random_user() if random.random() > 0.5 else "-"
    return f"{ts} {elapsed} {client} {code} {size} {method} {url} {user} DIRECT/{random_ip()} text/html"

# --- Postfix/sendmail style entries ---
postfix_events = [
    "status=sent (250 2.0.0 Ok: queued as {qid})",
    "status=bounced (host mail.{dom} said: 550 5.1.1 <{user}@{dom}>: Recipient address rejected)",
    "status=deferred (connect to mail.{dom}[{ip}]: Connection timed out)",
    "status=sent (250 2.0.0 Ok: queued as {qid}, relay={ip}:25)",
    "reject: RCPT from unknown[{ip}]: 554 5.7.1 Relay access denied",
]

def gen_postfix_log():
    qid = "".join(random.choices("0123456789ABCDEF", k=10))
    dom = random.choice(["example.com", "corp.local", "clientmail.net", "vendor.org"])
    user = random_user()
    ip = random_ip()
    template = random.choice(postfix_events)
    msg = template.format(qid=qid, dom=dom, user=user, ip=ip)
    return f"postfix/smtp[{random.randint(1000,9999)}]: {qid}: to=<{user}@{dom}>, relay={ip}[{ip}]:25, delay={random.uniform(0.1,5.0):.2f}, {msg}"

# --- CUPS style entries ---
cups_printers = ["HP_LaserJet_M404", "Canon_MX922", "Brother_HL2270DW", "Reception_Printer", "Warehouse_Label_Printer"]
cups_events = [
    "Print job {jid} queued by {user}",
    "Print job {jid} started on printer {printer}",
    "Print job {jid} completed successfully",
    "Print job {jid} stopped: {printer} out of paper",
    "Print job {jid} canceled by {user}",
    "Printer {printer} state changed to idle",
    "Printer {printer} state changed to processing",
]

def gen_cups_log():
    jid = random.randint(1000, 9999)
    user = random_user()
    printer = random.choice(cups_printers)
    template = random.choice(cups_events)
    return template.format(jid=jid, user=user, printer=printer)

GENERATORS = {
    "squid": gen_squid_log,
    "postfix": gen_postfix_log,
    "cups": gen_cups_log,
}

def send_sample_logs(count_per_facility=100, delay_seconds=2):
    # Build a flat list of (facility_name) repeated count_per_facility times each,
    # then shuffle so the three facilities interleave randomly.
    queue = []
    for name in GENERATORS:
        queue.extend([name] * count_per_facility)
    random.shuffle(queue)

    for i, name in enumerate(queue, start=1):
        msg = GENERATORS[name]()
        loggers[name].info(msg)
        print(f"[{i}/{len(queue)}] sent to {name} (local{list(FACILITIES.keys()).index(name)+1}): {msg[:80]}...")
        time.sleep(delay_seconds)

if __name__ == "__main__":
    send_sample_logs(count_per_facility=100, delay_seconds=2)
