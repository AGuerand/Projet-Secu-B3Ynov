import time
import re
from functools import wraps
from flask import request, abort
import logging
# Dictionnaire pour stocker les tentatives de connexion échouées
failed_attempts = {}

# Nombre de tentatives de connexion échouées autorisées avant le blocage
max_attempts = 5

# Temps en secondes avant qu'une tentative de connexion échouée expire
block_duration = 300

# Dictionnaire pour stocker les adresses IP bloquées et leurs temps de déblocage
blocked_ips = {}

# Expression régulière pour détecter les injections SQL
sql_injection_pattern = re.compile(r"('|\"|;|--|\b(?:SELECT|INSERT|UPDATE|DELETE|FROM|WHERE)\b)", re.IGNORECASE)

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

def detect_sql_injection(input_data):
    if sql_injection_pattern.search(input_data):
        return True
    return False

def log_and_protect(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        username = request.form.get('username')
        password = request.form.get('password')
        client_ip = request.remote_addr

        if is_ip_blocked(client_ip):
            abort(429, description="Your IP is temporarily blocked. Please try again later.")
            logging.warning(f"This IP: '{client_ip}' try to connect againt to this Account: '{username}'")

        if username and password:
            if detect_bruteforce_attack(username):
                logging.warning(f"Brute force attack detected for Account: '{username}' from IP: '{client_ip}'")
                block_ip(client_ip)
                abort(429, description="Too many failed attempts. Please try again later.")
            if detect_sql_injection(username) or detect_sql_injection(password):
                logging.warning(f"SQL injection detected from IP: '{client_ip}'. Account: '{username}', Password: '{password}'")
                block_ip(client_ip)
                abort(400, description="Malicious input detected.")

        return func(*args, **kwargs)
    return wrapper

