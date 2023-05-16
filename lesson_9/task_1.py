from ipaddress import ip_address
from subprocess import Popen, PIPE


def host_ping(list_ip_addresses, timeout=500, requests=1):
    results = {'Доступные узлы': "", 'Недоступные узлы': ""}
    for address in list_ip_addresses:
        try:
            address = ip_address(address)
        except ValueError:
            pass
        proc = Popen([f"ping", f'-t {timeout}', f'-c {requests}', f'{address}'], shell=False, stdout=PIPE)
        proc.wait()
        if proc.returncode == 0:
            results['Доступные узлы'] += f"{str(address)}\n"
            res_string = f'{address} - Узел доступен'
        else:
            results['Недоступные узлы'] += f"{str(address)}\n"
            res_string = f'{address} - Узел недоступен'
        print(res_string)
    return results


if __name__ == '__main__':
    ip_addresses = ['google.com', '8.8.8.8', '192.168.0.100', '192.168.0.167']
    host_ping(ip_addresses)
