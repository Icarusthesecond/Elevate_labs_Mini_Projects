import socket
import paramiko
import threading

host_key = paramiko.RSAKey.generate(2048)

log_file = "honeypot.log"

def log(msg):
    with open(log_file, "a") as f:
        f.write(msg + "\n")
    print(msg)

class Server(paramiko.ServerInterface):
    def check_auth_password(self, username, password):
        log(f"[LOGIN ATTEMPT] {username}:{password}")
        return paramiko.AUTH_SUCCESSFUL

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    # 🔥 ADD THIS (VERY IMPORTANT)
    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True

    def check_channel_shell_request(self, channel):
        return True

def handle_client(client):
    transport = paramiko.Transport(client)
    transport.add_server_key(host_key)

    server = Server()
    transport.start_server(server=server)

    chan = transport.accept(20)
    if chan is None:
        return

    chan.send(b"Welcome to Ubuntu 20.04 LTS\n")
    chan.send(b"login successful\n")

    while True:
        try:
            chan.send(b"\n$ ")
            command = chan.recv(1024).decode().strip()
            log(f"[COMMAND] {command}")

            if command.lower() == "exit":
                chan.send(b"logout\n")
                break

            elif command == "ls":
                chan.send(b"file1.txt  file2.txt\n")

            elif command == "pwd":
                chan.send(b"/home/user\n")

            elif command == "whoami":
                chan.send(b"user\n")

            else:
                chan.send(b"command not found\n")

        except:
            break

    chan.close()

def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("0.0.0.0", 2222))
    sock.listen(100)

    print("🔥 Honeypot running on port 2222...")

    while True:
        client, addr = sock.accept()
        log(f"[CONNECTION] {addr[0]}")
        threading.Thread(target=handle_client, args=(client,)).start()

# 🔥 VERY IMPORTANT (THIS LINE MUST EXIST)
start_server()
