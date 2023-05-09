import time
import re
import urllib.parse
import base64
from functools import wraps
from flask import request, abort, Flask
from flask_mail import Mail, Message
import logging
import re
from scapy.all import *

app = Flask(__name__)

app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'c5780b3c580502'
app.config['MAIL_PASSWORD'] = '32b8e070eab6c0'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)


# Dictionnaire pour stocker les tentatives de connexion échouées
failed_attempts = {}

# Dictionnaire pour stocker les tentatives de connexion échouées par IP
# failed_attempts_by_ip = {}

# Nombre de tentatives de connexion échouées autorisées avant le blocage
max_attempts = 7

# Temps en secondes avant qu'une tentative de connexion échouée expire
block_duration = 200

# Dictionnaire pour stocker les adresses IP bloquées et leurs temps de déblocage
blocked_ips = {}

# Expression régulière pour détecter les injections SQL
# sql_injection_pattern = re.compile(r"('|\"|;|--|\b(?:SELECT|INSERT|UPDATE|DELETE|FROM|WHERE)\b)", re.IGNORECASE)  (Regex V1)
# Regex V2 (+Puissant) from: https://regex101.com/library/qE9gR7
sql_injection_pattern = re.compile(r"\s*([\0\b\'\"\n\r\t\%\_\\]*\s*(((select\s*.+\s*from\s*.+)|(insert\s*.+\s*into\s*.+)|(update\s*.+\s*set\s*.+)|(delete\s*.+\s*from\s*.+)|(drop\s*.+)|(truncate\s*.+)|(alter\s*.+)|(exec\s*.+)|(\s*(all|any|not|and|between|in|like|or|some|contains|containsall|containskey)\s*.+[\=\>\<=\!\~]+.+)|(let\s+.+[\=]\s*.*)|(begin\s*.*\s*end)|(\s*[\/\*]+\s*.*\s*[\*\/]+)|(\s*(\-\-)\s*.*\s+)|(\s*(contains|containsall|containskey)\s+.*)))(\s*[\;]\s*)*)+")

# Durée de blocage en secondes
block_duration_ip = 300

def is_ip_blocked(client_ip):
    if client_ip in blocked_ips:
        block_expiration_time = blocked_ips[client_ip]
        if time.time() < block_expiration_time:
            return True
        else:
            del blocked_ips[client_ip]
            return False
    return False

def block_ip(client_ip):
    blocked_ips[client_ip] = time.time() + block_duration_ip

def decode_encoded_string(input_string):
    decoded_string = input_string

    # Décoder l'encodage URL
    try:
        decoded_string = urllib.parse.unquote(decoded_string)
    except Exception:
        pass

    # Décoder l'encodage Base64
    try:
        decoded_string = base64.b64decode(decoded_string).decode('utf-8')
    except Exception:
        pass

    return decoded_string


def detect_bruteforce_attack(username):
    current_time = int(time.time())
    if username not in failed_attempts:
        failed_attempts[username] = {"attempts": 1, "time": current_time}
    else:
        if current_time - failed_attempts[username]["time"] < block_duration:
            failed_attempts[username]["attempts"] += 1
        else:
            failed_attempts[username] = {"attempts": 1, "time": current_time}

    if failed_attempts[username]["attempts"] >= max_attempts:
        return True
    return False

def detect_xss(input_string):
#    xss_pattern = r'<.*?>|&.*?;'
# XSS Regex V2
    xss_pattern = r'(\b)(on\S+)(\s*)=|javascript|<(|\/|[^\/>][^>]+|\/[^>][^>]+)>'
    return bool(re.search(xss_pattern, input_string))

def detect_sql_injection(input_data):
    decoded_input_data = decode_encoded_string(input_data)
    if sql_injection_pattern.search(input_data):
        return True
    elif sql_injection_pattern.search(decoded_input_data):
        return True
    return False

def detect_cybersecurity_agents(user_agent):
    cybersecurity_agents = ['nikto', 'burp', 'metasploit']
    user_agent = user_agent.lower()
    return any(agent in user_agent for agent in cybersecurity_agents)

def detect_metasploit(pkt):
    if TCP in pkt:
        client_ip = request.remote_addr
        if pkt[TCP].dport == 4444 or pkt[TCP].dport == 4445:
            if "metasploit" in str(pkt[TCP].payload).lower():
                print("Metasploit traffic detected!")          
                logging.warning(f"Cybersecurity agent Metasploit detected from IP '{client_ip}'")
                block_ip(client_ip)
                abort(400, description="Access denied.")

# def update_failed_attempts_by_ip(client_ip):
#     if client_ip not in failed_attempts_by_ip:
#         failed_attempts_by_ip[client_ip] = 1
#     else:
#         failed_attempts_by_ip[client_ip] += 1


def log_and_protect(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        username = request.form.get('username')
        password = request.form.get('password')
        client_ip = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        
        if is_ip_blocked(client_ip):
            abort(429, description="Your IP is temporarily blocked. Please try again later.")
            msg = Message('Ip blocked', sender =   'idsynov@gmail', recipients = ['ids@gmail.com'])
            msg.body = f"This IP: '{client_ip}' try to connect againt to this Account: '{username}'"
            mail.send(msg)
            logging.warning(f"This IP: '{client_ip}' try to connect againt to this Account: '{username}'")

        if detect_cybersecurity_agents(user_agent):
            msg = Message('Agents detected', sender =   'idsynov@gmail', recipients = ['ids@gmail.com'])
            msg.body = f"Cybersecurity agent '{user_agent}' detected from IP '{client_ip}'"
            mail.send(msg)
            logging.warning(f"Cybersecurity agent '{user_agent}' detected from IP '{client_ip}'")
            block_ip(client_ip)
            abort(400, description="Access denied.")

        if username and password:
            if detect_bruteforce_attack(username):
                msg = Message('Bruteforce detected', sender =   'idsynov@gmail', recipients = ['ids@gmail.com'])
                msg.body = f"Brute force attack detected for Account: '{username}' from IP: '{client_ip}'"
                mail.send(msg)
                logging.warning(f"Brute force attack detected for Account: '{username}' from IP: '{client_ip}'")
                block_ip(client_ip)
                abort(429, description="Too many failed attempts. Please try again later.")

            if detect_sql_injection(username) or detect_sql_injection(password):
                msg = Message('SQL Injection detected', sender =   'idsynov@gmail', recipients = ['ids@gmail.com'])
                msg.body = f"SQL injection detected from IP: '{client_ip}'. Account: '{username}', Password: '{password}'"
                mail.send(msg)
                logging.warning(f"SQL injection detected from IP: '{client_ip}'. Account: '{username}', Password: '{password}'")
                block_ip(client_ip)
                abort(400, description="Malicious input detected.")

            if detect_xss(username) or detect_xss(password):
                msg = Message('XSS detected', sender =   'idsynov@gmail', recipients = ['ids@gmail.com'])
                msg.body = f"XSS attack detected from IP: '{client_ip}'. Account: '{username}', Password: '{password}'"
                mail.send(msg)
                logging.warning(f"XSS attack detected from IP: '{client_ip}'. Account: '{username}', Password: '{password}'")
                block_ip(client_ip)
                abort(400, description="Malicious input detected.")
        # if username and password:
        #     user = User.query.filter_by(username=username).first()
        #     if not user or user.password != password:
        #         update_failed_attempts_by_ip(client_ip)
        return func(*args, **kwargs)
     #sniff(filter="tcp port 4444 or tcp port 4445", prn=detect_metasploit)
    return wrapper
