import datetime
import pytz
import subprocess

LOG_FILE = '/home/thony/flaskapp/log.log'
MAX_LOGIN_ATTEMPTS = 5
TIME_FRAME_SECONDS = 60


def parse_log_file():
    login_attempts = {}
    with open(LOG_FILE) as log_file:
        for line in log_file:
            fields = line.strip().split(' - ')
            if len(fields) != 4:
                continue
            timestamp_str, _, log_level, message = fields
            if log_level != 'INFO' or 'Login' not in message or 'successful' not in message:

                continue
            words = message.split()
            if len(words) < 7:
                continue
            username, _, _, _, _, _, ip_address = words[-7:]
            key = (username, ip_address)
            timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%d %H%d %H:%M:%S,%f')
            if key not in login_attempts:
                login_attempts[key] = []
            login_attempts[key].append(timestamp)
    return login_attempts

def detect_brute_force(login_attempts):
    for key, timestamps in login_attempts.items():
        if len(timestamps) >= MAX_LOGIN_ATTEMPTS:
            last_attempt_time = timestamps[-1]
            first_attempt_time = timestamps[-MAX_LOGIN_ATTEMPTS]
            time_frame = last_attempt_time - first_attempt_time
            if time_frame.seconds <= TIME_FRAME_SECONDS:
                tz = pytz.timezone('Europe/Paris')
                last_attempt_time = last_attempt_time.astimezone(tz)
                now = datetime.datetime.now(tz)
                if (now - last_attempt_time).seconds <= TIME_FRAME_SECONDS:
                    print(f"Brute force attack detected for user {key[0]} from from IP {key[1]} at {last_attempt_time:%Y-%m-%d %H:%M:%S %Z}")
                    # Add code here to block the IP address or take other measu>

                    ip_address = key[1]
                    command = f'iptables -I INPUT -s {ip_address} -j DROP && sleep 60 && iptables -D INPUT -s {ip_address} -j DROP'

                    subprocess.run(command, shell=True, check=True)

if __name__ == '__main__':
    login_attempts = parse_log_file()
    detect_brute_force(login_attempts)