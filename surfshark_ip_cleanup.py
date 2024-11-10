import csv
import os
import datetime

TEMP_FILE = 'surfshark_ips_temp.csv'
MAIN_FILE = 'surfshark_ips.csv'
NEW_IPS_FILE = 'new_surfshark_ips.csv'

def read_csv(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return list(csv.reader(f))
    return []

def write_csv(file_path, header, data):
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)

def read_existing_ips(file_path):
    exs_ip_data = {}
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                exs_ip_data[row['IP']] = {
                    'First Seen': row['First Seen'],
                    'Last Seen': row['Last Seen']
                }
    return exs_ip_data

def main():
    temp_data = read_csv(TEMP_FILE)
    if not temp_data:
        print(f"The file '{TEMP_FILE}' does not exist.")
        return

    # Remove the header and duplicates
    ips = list(set(row[0] for row in temp_data[1:]))

    # Ensure the main file exists with the correct header
    if not os.path.exists(MAIN_FILE):
        write_csv(MAIN_FILE, ["IP", "First Seen", "Last Seen"], [])

    exs_ip_data = read_existing_ips(MAIN_FILE)
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_ips = []

    # Update the dictionary with the new data
    for ip in ips:
        if ip in exs_ip_data:
            exs_ip_data[ip]['Last Seen'] = current_time
        else:
            exs_ip_data[ip] = {'First Seen': current_time, 'Last Seen': current_time}
            new_ips.append([ip, current_time, current_time])

    # Write the updated data to the main file
    updated_data = [[ip, times['First Seen'], times['Last Seen']] for ip, times in exs_ip_data.items()]
    write_csv(MAIN_FILE, ["IP", "First Seen", "Last Seen"], updated_data)

    # Write the new IPs to a separate file
    if new_ips:
        write_csv(NEW_IPS_FILE, ["IP", "First Seen", "Last Seen"], new_ips)

if __name__ == "__main__":
    main()
