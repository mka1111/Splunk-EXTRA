Sure 👍 Let’s go step by step.
You want to **forward all incoming traffic on port 9997** on your Linux host to **10.0.1.1:9997** (which is probably another machine in your internal network).
This is a classic **port forwarding (DNAT)** setup using `iptables`.

---

### 🧭 1. Enable IP forwarding

Before you start, make sure your system allows forwarding between interfaces:

```bash
echo 1 > /proc/sys/net/ipv4/ip_forward
```

To make it permanent, edit `/etc/sysctl.conf` and ensure you have:

```bash
net.ipv4.ip_forward = 1
```

Then apply the change:

```bash
sysctl -p
```

---

### ⚙️ 2. Add the DNAT (Destination NAT) rule

Let’s assume:

* External interface (receiving traffic): `eth0`
* Internal network interface: `eth1`
* Destination host: `10.0.1.1`
* Port: `9997`

Run:

```bash
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 9997 -j DNAT --to-destination 10.0.1.1:9997
```

✅ This means:

> "When TCP traffic comes in on `eth0` and port `9997`, rewrite its destination to `10.0.1.1:9997`."

---

### 🔁 3. Allow forwarding of the traffic

Add a FORWARD rule to allow the packets to pass through:

```bash
iptables -A FORWARD -p tcp -d 10.0.1.1 --dport 9997 -j ACCEPT
```

---

### 🧩 4. (Optional) MASQUERADE if needed

If `10.0.1.1` doesn’t have a route back to your external client, you need **source NAT** on the outgoing interface:

```bash
iptables -t nat -A POSTROUTING -o eth1 -p tcp -d 10.0.1.1 --dport 9997 -j MASQUERADE
```

This rewrites the source IP to the Linux machine’s IP so that responses return correctly.

---

### 🧱 5. Save and persist rules

On most systems:

```bash
iptables-save > /etc/iptables/rules.v4
```

or use:

```bash
service iptables save
```

---

### ✅ Quick Summary

| Step | Command                                         | Purpose                       |
| ---- | ----------------------------------------------- | ----------------------------- |
| 1    | `echo 1 > /proc/sys/net/ipv4/ip_forward`        | Enable forwarding             |
| 2    | `iptables -t nat -A PREROUTING ... DNAT`        | Redirect port 9997            |
| 3    | `iptables -A FORWARD ... ACCEPT`                | Allow forwarding              |
| 4    | `iptables -t nat -A POSTROUTING ... MASQUERADE` | Fix reply routing (if needed) |
| 5    | `iptables-save`                                 | Persist rules                 |

---

Would you like me to also show the **equivalent `nftables` configuration** (modern replacement for `iptables`)?





Good — you want to **verify that traffic is arriving on TCP port 9997** using `tcpdump`.
Here’s exactly how to do it 👇

---

### 🧭 Basic command

To capture **incoming TCP traffic on port 9997**:

```bash
sudo tcpdump -i any tcp port 9997
```

**Explanation:**

* `sudo` — needed because tcpdump requires root privileges.
* `-i any` — listen on **all network interfaces** (you can replace it with a specific one, e.g. `eth0`).
* `tcp port 9997` — filters only TCP packets using port 9997 (source or destination).

---

### 🎯 Capture only *incoming* packets (destination port 9997)

If you want only **packets coming to** port 9997 (not responses):

```bash
sudo tcpdump -i eth0 'tcp dst port 9997'
```

**Explanation:**

* `dst port 9997` — only shows packets whose **destination** port is 9997.
* Replace `eth0` with your actual interface if needed.

---

### 🧩 Optional — verbose and readable output

To see more details:

```bash
sudo tcpdump -i eth0 -nvvv 'tcp dst port 9997'
```

**Flags:**

* `-n` — don’t resolve hostnames (faster).
* `-v`, `-vv`, `-vvv` — more verbose each time.

---

### 💾 Save capture to a file for later analysis

If you want to analyze it in Wireshark:

```bash
sudo tcpdump -i eth0 'tcp port 9997' -w /tmp/port9997.pcap
```

Then you can open `/tmp/port9997.pcap` in Wireshark.

---

### ✅ Quick Summary

| Purpose                       | Command                                                      |
| ----------------------------- | ------------------------------------------------------------ |
| View all traffic on port 9997 | `sudo tcpdump -i any tcp port 9997`                          |
| Only incoming (dst port)      | `sudo tcpdump -i eth0 'tcp dst port 9997'`                   |
| Detailed view                 | `sudo tcpdump -i eth0 -nvvv 'tcp dst port 9997'`             |
| Save to file                  | `sudo tcpdump -i eth0 'tcp port 9997' -w /tmp/port9997.pcap` |

---

Would you like me to show how to **verify that packets are being forwarded correctly** to `10.0.1.1` (i.e., test both pre- and post-DNAT traffic)?
