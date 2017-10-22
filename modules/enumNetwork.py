
import nmap

def run(**args):
    nm = nmap.PortScanner()
    output = ""
    nm.scan(hosts='10.0.0.0/24')
    hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
    for host, status in hosts_list:
        output = output + ('{0}:{1}'.format(host, status))
    return output
