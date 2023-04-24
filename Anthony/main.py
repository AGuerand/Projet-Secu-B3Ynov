import datetime
import pytz
import subprocess

log_file = '/home/thony/flaskapp/log.log'
max_login = 5
time_to_detect = 30


def parse_log():
    login_attempts = {}
    with open(log_file) as file:
        for line in file:
            #Separate logs
            fields = line.strip().split(' - ')
            if len(fields) != 4:
                continue
            timestamp_str, _, log_level, message = fields
            #filter out successful login
            if log_level != 'INFO' or 'Login' not in message or 'successful' not in message:

                continue
            words = message.split()
            #if log is correctly written
            if len(words) < 7:
                continue
            #select what will be used to make the log
            username, _, _, _, _, _, ip_address = words[-7:]
            key = (username, ip_address)
            #select the time stamp
            timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f')
            if key not in login_attempts:
                login_attempts[key] = []
            login_attempts[key].append(timestamp)
    return login_attempts

def detect_brute_force(login_attempts):
    for key, timestamps in login_attempts.items():
        #configure the parrameter for the attempt in time
        if len(timestamps) >= max_login:
            last_attempt_time = timestamps[-1]
            first_attempt_time = timestamps[-max_login]
            time_frame = last_attempt_time - first_attempt_time
            if time_frame.seconds <= time_to_detect:
                tz = pytz.timezone('Europe/Paris')
                last_attempt_time = last_attempt_time.astimezone(tz)
                now = datetime.datetime.now(tz)
                if (now - last_attempt_time).seconds <= time_to_detect:
                    #log
                    print(f"Brute force attack detected for user {key[0]} from from IP {key[1]} at {last_attempt_time:%Y-%m-%d %H:%M:%S %Z}")
                    # block the IP address

                    ip_address = key[1]
                    command = f'iptables -I INPUT -s {ip_address} -j DROP && sleep 60 && iptables -D INPUT -s {ip_address} -j DROP'

                    subprocess.run(command, shell=True, check=True)

if __name__ == '__main__':
    login_attempts = parse_log()
    detect_brute_force(login_attempts)