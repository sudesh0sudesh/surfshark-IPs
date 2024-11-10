import dns.resolver
import os
import requests

DNS_SERVERS = ['8.8.8.8', '8.8.4.4']
DOMAIN_FILE = 'surfshark.txt'
OUTPUT_FILE = 'surfshark_subnet.txt'
IP_GUIDE_URL = "https://ip.guide/"

def configure_dns_resolver():
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = DNS_SERVERS
    return resolver

def read_domains_from_file(file_path):
    if not os.path.exists(file_path):
        print(f"The file '{file_path}' does not exist.")
        exit(1)
    with open(file_path) as f:
        return [line.strip() for line in f]

def fetch_subnet_for_ip(ip):
    try:
        response = requests.get(f"{IP_GUIDE_URL}{ip}", timeout=5)
        if response.status_code == 200:
            subnet = response.json().get('network', {}).get('cidr', None)
            if not subnet:
                raise ValueError("Invalid response format")
        else:
            raise ValueError(f"Received status code {response.status_code}")
    except Exception as e:
        print(f"Error fetching subnet for IP {ip}: {e}")
        ip_split = str(ip).split('.')
        subnet = f"{'.'.join(ip_split[:3])}.0/24"
    return subnet

def resolve_domains_to_subnets(domains, resolver):
    ip_subnet = set()
    for domain in domains:
        print(f"Resolving domain: {domain}")
        try:
            temp_ips=set()
            for i in range(0,10):
                answers = resolver.resolve(domain, 'A')
                for ip in answers:
                    temp_ips.add(str(ip))
            for ip in temp_ips:
                subnet = fetch_subnet_for_ip(ip)
                print(f"Subnet: {subnet}")
                ip_subnet.add(subnet)
        except Exception as e:
            print(f"Error resolving {domain}: {e}")
    return ip_subnet

def write_subnets_to_file(subnets, file_path):
    with open(file_path, 'w') as f:
        for item in subnets:
            f.write(f"{item}\n")

def main():
    resolver = configure_dns_resolver()
    domains = read_domains_from_file(DOMAIN_FILE)
    subnets = resolve_domains_to_subnets(domains, resolver)
    write_subnets_to_file(subnets, OUTPUT_FILE)

if __name__ == "__main__":
    main()
