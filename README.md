# Projet Final B3 Cybersécurité Paris Ynov Campus 2023- WAF Securisation de la couche 7(Application)

Ce projet vise à améliorer la sécurité de la partie application de Open Systems Interconnection en locurence le protocole HTTP qui est utilisé pour la communication entre les client Web et les serveurs. Pour un deployment simplifié stable on ce base sur le framework de dev. Web Flask, le but de l'exercice est de deployer un eventaille de techniques et fonctionnalitées de securité pour pré-munir les actions malveillantes lié à la couche 7, en détectant et bloquant les attaques par force brute, les injections SQL, les ataques XSS et Les agents d'automatisation d'attaque connu en Cyber-Sécurité. ET fournir également un système de logging pour garder une trace des requêtes malveillantes et des adresses IP associées, comportement correspondant à un WAF (Web Application Firewall).

## Membres de l'equipe
- Castellanos Jorge
- Azzam Nesrine
- Guerand Anthony
- Razafindriantsoa Marc

## Fonctionnalités

- Détection des attaques par force brute
- Détection des injections SQL basiques
- Détection des attaques XSS
- Détection des agents de cybersécurité connus
- Blocage temporaire des adresses IP responsables des attaques détectées
- Enregistrement des requêtes suspectes, y compris l'heure, la date et l'adresse IP de l'émetteur

## Dépendances

- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF
- Scapy

## Installation

1. Clonez ce dépôt ou téléchargez les fichiers `app.py` et `http_logger.py`.
2. Installez les dépendances en exécutant la commande suivante :

```bash
pip install Flask Flask-SQLAlchemy Flask-Login scapy
```
3. Donner les droits suffissant au programme pour analyser les ports :

```bash
su
```

4. Exécutez l'application avec la commande :

```bash
python app.py
```

L'application sera accessible à l'adresse `http://127.0.0.1:5000`.

## Utilisation

Les routes `login` et `register` de l'application sont protégées par le décorateur `log_and_protect`. Ce décorateur vérifie les tentatives de connexion échouées pour détecter les attaques par force brute et analyse les entrées utilisateur pour détecter les injections SQL.

Si une attaque est détectée, l'adresse IP de l'émetteur est bloquée temporairement pendant 5 minutes, et un message d'erreur est renvoyé. Les requêtes suspectes sont enregistrées dans un fichier `http_requests.log`, y compris l'heure, la date et l'adresse IP de l'émetteur.

## Structure des fichiers

- `app.py` : fichier principal de l'application Flask, contenant les routes, les modèles de base de données et les configurations.
- `forms.py` : définition des formulaires de connexion et d'enregistrement avec les validateurs appropriés.
- `http_logger.py` : fonctions de protection et de journalisation des requêtes HTTP. Implémente la détection des attaques et le blocage des adresses IP.
- `templates` : dossier contenant les modèles HTML pour les pages de connexion et d'enregistrement.
- `http_requests.log` : fichier de journalisation des requêtes HTTP (sera créé automatiquement lors de l'exécution de l'application).

## Personnalisation

Vous pouvez personnaliser les paramètres de sécurité en modifiant les variables globales dans `http_logger.py` :

- `max_attempts`: Nombre de tentatives de connexion échouées autorisées avant le blocage (par défaut : 5)
- `block_duration`: Temps en secondes avant qu'une tentative de connexion échouée expire (par défaut : 300)
- `block_duration_ip`: Durée de blocage en secondes pour une adresse IP (par défaut : 300)

## Avertissement

Veuillez noter que l'approche utiliser peut ne pas être à 100 % fiable, car elles se bases sur les caracteristiques simples pour identifier les différentes types de attaques, certaines attaques avancé peuvent avoir raison de cette securité.
Par exemple:
- La détection des agents connues en cyber est simpliste, elle ce base sur la frequence et l'en-tête User-Agent des requetes http, mais les attaquants peuvent facilement modifier l'en-tête User-Agent pour contourner la détection.
- La détection des injections SQL dans ce projet est rudimentaire et pourrait ne pas couvrir tous les cas possibles. Pour une protection plus robuste, l'utilisation des bibliothèques spécialisées ou des services de sécurité Web est plus approprié.

## CREDIT/SOURCE

Pour réaliser ce projet, voici une liste de ressources et de documentations utilisé :

1. **Flask** : Le framework web Python utilisé pour développer l'application.
   - Documentation officielle : https://flask.palletsprojects.com/en/2.1.x/
   - Guide de démarrage rapide : https://flask.palletsprojects.com/en/2.1.x/quickstart/
   - HTML Template : https://flask.palletsprojects.com/en/1.1.x/patterns/templateinheritance/
   - Tutoriel Flask (Mega-Tutorial) : https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

2. **Flask-SQLAlchemy** : L'extension Flask pour interagir avec des bases de données SQL.
   - Documentation officielle : https://flask-sqlalchemy.palletsprojects.com/en/2.x/
   - Tutoriel Flask-SQLAlchemy : https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/

3. **Flask-Login** : L'extension Flask pour gérer les sessions utilisateurs.
   - Documentation officielle : https://flask-login.readthedocs.io/en/latest/
   - Exemple d'utilisation de Flask-Login : https://github.com/shekhargulati/flask-login-example

4. **WTForms** : Une bibliothèque Python pour gérer les formulaires web.
   - Documentation officielle : https://wtforms.readthedocs.io/en/3.0.x/
   - Guide d'utilisation de WTForms avec Flask : https://flask.palletsprojects.com/en/2.1.x/patterns/wtforms/

6. **SQLite** : Le système de base de données SQL utilisé pour stocker les informations des utilisateurs.
   - Documentation officielle : https://www.sqlite.org/docs.html
   - Guide d'utilisation de SQLite avec Python : https://docs.python.org/3/library/sqlite3.html

7. **Sécurité web** : Ressources pour comprendre les attaques par force brute, les injections SQL, les attaques XSS et les agents de cybersécurité.
   - OWASP (Open Web Application Security Project) : https://owasp.org/
   - OWASP Top Ten Project : https://owasp.org/www-project-top-ten/
   - Attaques par force brute : https://owasp.org/www-community/controls/Blocking_Brute_Force_Attacks
   - Injections SQL : https://owasp.org/www-community/attacks/SQL_Injection
                      https://regex101.com/library/qE9gR7
   - Attaques XSS : https://owasp.org/www-community/attacks/xss/
                    https://www.regextester.com/110397
   - Burp Agent Détection: https://blog.cyberseer.net/how-cyberseer-detect-burp-suite-using-darktrace
   - Metasploit Agent Détection: https://github.com/secdev/scapy
   - WAF Definition: https://www.crowdstrike.fr/cybersecurity-101/web-application-firewall/
   - WAF Application Exemple (Open Source): https://github.com/0xInfection/Awesome-WAF
