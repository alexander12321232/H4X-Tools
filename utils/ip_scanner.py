import socket
import time
from colorama import Fore

class scan:
    def __init__(self, ip):
        ip_add = socket.gethostbyname(ip)
        try:
            for i in range (10,100,10):
                time.sleep(2)
                print("Loading", i, "%")
            print("\t [*] Successfully connected with the Server........!")
            for j in range (0,5):
                time.sleep(2)
                print("[*] Scanning for the IP address...")
            print ("[*] IP Address Found ...!")
            time .sleep(5)
            for k in range (0,4):
                time.sleep(5)
                print("[*] Decoding")
            print("\t [*] IP ADDRESS OF THE WEBSITE : \t ", ip_add)
        except Exception as e:
            print(f"\t{Fore.RED}[*] Can't connect to the server" + Fore.RESET)    