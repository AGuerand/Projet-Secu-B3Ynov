import datetime

log_File = "../../log.log"
login_Num = 10
login_Time = 10

def parse_log_file():
    login_attempts = {}
    with open(log_File) as log_file:
        for line in log_file:
            if "Login" in line and "successful" in line:
                words = line.strip().split()
                if len(words) >= 11:
                    username = words[-7]
                    ip_address = words[-1]
                    key = (username, ip_address)
                    timestamp = datetime.datetime.strptime(words[0], '%Y-%m-%d %H:%M:%S,%f')
                    if key not in login_attempts:
                        login_attempts[key] = []
                    login_attempts[key].append(timestamp)
    return login_attempts

def detect_brute_force(login_attempts):
    for key, timestamps in login_attempts.items():
        if len(timestamps) >= login_Num:
            time_frame = timestamps[-1] - timestamps[0]
            if time_frame.seconds <= login_Time:
                print(f"Brute force attack detected for user {key[0]} from IP {key[1]}")
                # Add code here to block the IP address or take other measures

if __name__ == '__main__':
    login_attempts = parse_log_file()
    detect_brute_force(login_attempts)