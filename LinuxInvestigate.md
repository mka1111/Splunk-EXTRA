
To find what's making those port-8000 attempts:

bash
ss -tanp | grep 55410

or catch it live:

bash
ss -tanp state syn-sent

If the process has already given up by the time you look, this will catch it as it happens:

bash
watch -n 0.5 'ss -tanp | grep ":8000"'

Your logging setup is done and persisted — this is just the first thing it caught.

<img width="1784" height="118" alt="image" src="https://github.com/user-attachments/assets/241afa66-0d57-41b7-b997-b67eebc98bfd" />

# What is it and where does it live?
ls -l /proc/1327/exe
cat /proc/1327/cmdline | tr '\0' ' '; echo


<img width="884" height="183" alt="image" src="https://github.com/user-attachments/assets/c32e1b9d-97d8-4ef6-9581-0cdd9499159e" />


# Who started it, and when?

<img width="946" height="249" alt="image" src="https://github.com/user-attachments/assets/8c4fa1d6-c965-492d-89b0-e525701a05ad" />


  ps -o pid,ppid,user,lstart,cmd -p 1327
  ps -o pid,ppid,user,cmd -p $(awk '{print $4}' /proc/1327/stat)

# Is it from a package, or unmanaged?
dpkg -S "$(readlink -f /proc/1327/exe)" 2>/dev/null || echo "NOT owned by any package"
<img width="993" height="211" alt="image" src="https://github.com/user-attachments/assets/6202014e-64b7-4fde-8e2c-b2fbb924939d" />

# Is it a service?
systemctl status 1327 2>/dev/null | head -20
<img width="1719" height="481" alt="image" src="https://github.com/user-attachments/assets/927aab3e-ae4b-4f7c-9567-1cb7ad8dc327" />





# What else does it have open?
ls -l /proc/1327/fd 2>/dev/null | head -30

<img width="913" height="394" alt="image" src="https://github.com/user-attachments/assets/61e9d485-7e65-4a04-94c8-040f9df1966c" />

