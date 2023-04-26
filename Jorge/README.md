# Projet Final B3 Cybersécurité Paris Ynov Campus 2023- Securisation de la couche 7(Application)

Ce projet vise à améliorer la sécurité de la partie application de Open Systems Interconnection en locurence le protocole HTTP qui est utilisé pour la communication entre les client Web et les serveurs. Pour un deployment simplifié stable on ce base sur le framework de dev. Web Flask, le but de l'exercice est de deployer un eventaille de techniques et fonctionnalitées de securité pour pré-munir les actions malveillantes lié à la couche 7, en détectant et bloquant les attaques par force brute et les injections SQL. ET fournir également un système de logging pour garder une trace des requêtes malveillantes et des adresses IP associées.

## Membres de l'equipe
- Castellanos Jorge
- Azzam Nesrine
- Guerand Anthony
- Razafindriantsoa

## Fonctionnalités

- Détection des attaques par force brute
- Détection des injections SQL basiques
- Blocage temporaire des adresses IP responsables des attaques détectées
- Enregistrement des requêtes suspectes, y compris l'heure, la date et l'adresse IP de l'émetteur

## Dépendances

- Flask
- Flask-SQLAlchemy
- Flask-Login

## Installation

1. Clonez ce dépôt ou téléchargez les fichiers `app.py` et `http_logger.py`.
2. Installez les dépendances en exécutant la commande suivante :

```bash
pip install Flask Flask-SQLAlchemy Flask-Login
```

3. Exécutez l'application avec la commande :

```bash
python app.py
```

L'application sera accessible à l'adresse `http://127.0.0.1:5000`.

## Utilisation

Les routes `login` et `register` de l'application sont protégées par le décorateur `log_and_protect`. Ce décorateur vérifie les tentatives de connexion échouées pour détecter les attaques par force brute et analyse les entrées utilisateur pour détecter les injections SQL.

Si une attaque est détectée, l'adresse IP de l'émetteur est bloquée temporairement pendant 5 minutes, et un message d'erreur est renvoyé. Les requêtes suspectes sont enregistrées dans un fichier `http_requests.log`, y compris l'heure, la date et l'adresse IP de l'émetteur.

## Personnalisation

Vous pouvez personnaliser les paramètres de sécurité en modifiant les variables globales dans `http_logger.py` :

- `max_attempts`: Nombre de tentatives de connexion échouées autorisées avant le blocage (par défaut : 5)
- `block_duration`: Temps en secondes avant qu'une tentative de connexion échouée expire (par défaut : 300)
- `block_duration_ip`: Durée de blocage en secondes pour une adresse IP (par défaut : 300)

## Avertissement

La détection des injections SQL dans ce projet est rudimentaire et pourrait ne pas couvrir tous les cas possibles. Pour une protection plus robuste, envisagez d'utiliser des bibliothèques spécialisées ou des services de sécurité Web.