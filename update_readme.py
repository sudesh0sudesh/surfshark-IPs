import csv
import datetime

NEW_IPS_FILE = 'new_surfshark_ips.csv'
README_FILE = 'README.md'

def read_new_ip_count(file_path):
    if not os.path.exists(file_path):
        return 0
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        return sum(1 for row in reader)

def update_readme(file_path, new_ip_count):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(file_path, 'r') as f:
        lines = f.readlines()

    with open(file_path, 'w') as f:
        for line in lines:
            if line.startswith('Last Execution:'):
                f.write(f'Last Execution: {current_time}\n')
            elif line.startswith('New IP Count:'):
                f.write(f'New IP Count: {new_ip_count}\n')
            else:
                f.write(line)

def main():
    new_ip_count = read_new_ip_count(NEW_IPS_FILE)
    update_readme(README_FILE, new_ip_count)

if __name__ == "__main__":
    main()
