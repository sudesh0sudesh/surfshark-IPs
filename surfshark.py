import dns.resolver
import os

def configure_dns_resolver():
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = ['8.8.8.8', '8.8.4.4']
    return resolver

def read_domains_from_file(file_path):
    if not os.path.exists(file_path):
        print(f"The file '{file_path}' does not exist.")
        exit(1)
    with open(file_path) as f:
        return [line.strip() for line in f]

def resolve_domains_to_subnets(domains, resolver):
    ip_subnet = set()
    for domain in domains:
        print(domain)
        try:
            answers = resolver.resolve(domain, 'A')
            for ip in answers:
                ip_split = str(ip).split('.')
                ip_joined = f"{'.'.join(ip_split[:3])}.0/24"
                print(ip_joined)
                ip_subnet.add(ip_joined)
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout) as e:
            print(f"Error resolving {domain}: {e}")
    return ip_subnet

def write_subnets_to_file(subnets, file_path):
    with open(file_path, 'w') as f:
        for item in subnets:
            f.write(f"{item}\n")

def main():
    resolver = configure_dns_resolver()
    domains = read_domains_from_file('surfshark.txt')
    subnets = resolve_domains_to_subnets(domains, resolver)
    write_subnets_to_file(subnets, 'surfshark_subnet.txt')

if __name__ == "__main__":
    main()