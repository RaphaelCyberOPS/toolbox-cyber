# Pentest Toolbox par HackMeRaphael

## Introduction

Bienvenue dans le Pentest Toolbox, un projet développé dans le cadre de mon programme de Master en Cybersécurité.

Cet outil est conçu pour automatiser les tests de pénétration professionnels. Il consolide les résultats de divers scans dans un rapport PDF bien structuré, facilitant ainsi la revue et la résolution des vulnérabilités par les professionnels de la sécurité.

Développée en **Python et fonctionnant sous Windows**, cette application est facilement accessible et utilisable sans connaissance préalable en cybersécurité. Cependant, l'interprétation des résultats peut être complexe sans expertise en la matière.

## Fonctionnalités

### 1. Scan Nmap
L'outil s'intègre avec Nmap pour effectuer des analyses réseau et recueillir des informations sur les ports ouverts, les services et les versions, tout en collectant les CVE (Common Vulnerabilities and Exposures) associées grâce au script vulners.

### 2. Scan Web
L'outil traite les résultats des scanners d'applications web, spécifiquement SQLMap et Nikto, fournissant des insights détaillés sur les vulnérabilités potentielles des applications web.

- **SQLMap** : Un outil de test de pénétration open-source qui automatise la détection et l'exploitation des failles d'injection SQL, permettant de prendre le contrôle des serveurs de bases de données. L'intégration de SQLMap permet d'identifier les vulnérabilités d'injection SQL et d'aider à sécuriser les applications web.
  - **Information** : Projet SQLMap cloné depuis [GitHub - SQLMap](https://github.com/sqlmapproject/sqlmap).

- **Nikto** : Un scanner de serveur web open-source qui effectue des tests complets contre les serveurs web pour plus de 6700 fichiers/CGI potentiellement dangereux, versions obsolètes et problèmes spécifiques à certaines versions. L'intégration de Nikto permet d'identifier diverses vulnérabilités dans les serveurs et applications web.
  - **Information** : Projet Nikto cloné depuis [GitHub - Nikto](https://github.com/sullo/nikto).

### 3. Brute Force SSH
Cette fonctionnalité capture et rapporte les résultats des attaques par force brute SSH, y compris les ports testés, les listes de noms d'utilisateur et de mots de passe, ainsi que les résultats des tests.

### 4. Tests Réseau
Le toolbox utilise Scapy pour inclure divers tests réseau visant à identifier les vulnérabilités et les problèmes de sécurité potentiels au sein de l'infrastructure réseau. Ces tests incluent :
- **Attaque SYN Flood** : Envoie un grand nombre de paquets SYN à tous les ports actifs. **Un outil externe (comme Wireshark) est nécessaire pour voir l'impact sur la cible.**
- **Paquet Malformé** : Envoie des paquets avec différents drapeaux (comme URG, S, etc.) pour trouver des failles de sécurité ou des configurations particulières sur certains ports.

### 5. Génération et Test de Mots de Passe
L'outil inclut des fonctionnalités liées aux mots de passe :
- **Génération de Mots de Passe** : Génère des mots de passe sécurisés selon des critères définis (longueur, caractères spéciaux, etc.).
- **Test de Robustesse des Mots de Passe** : Attribue une note sur 5 au mot de passe entré, basée sur des critères tels que la longueur et la présence de chiffres.

### 6. Cartographie
L'outil offre des fonctions de cartographie du réseau local en scannant les hôtes, listant tous les hôtes actifs avec leur nom d'hôte et adresse MAC si possible. Il crée ensuite une carte pour représenter visuellement la structure du réseau et identifier les points critiques.

### 7. Génération de Rapport PDF
Toutes les données collectées sont compilées dans un rapport PDF, incluant les résultats de chaque scan effectué.

## Prérequis

- **Python** : Assurez-vous d'avoir Python (version 3.10 ou 3.11) installé sur votre système.
- ! Attention la version de python 3.12 ne fonctionnera pas ! Téléchargez-la version 3.11 depuis [python.org](https://www.python.org/downloads/).
- **pip** : Assurez-vous d'avoir pip installé pour gérer les packages Python.
- **Nmap** : Téléchargez et installez Nmap depuis [nmap.org](https://nmap.org/download.html).
- **Perl** : Certains outils peuvent nécessiter Perl (pour Nikto). Téléchargez-le depuis [perl.org](https://www.perl.org/get.html).

## Installation

1. **Clonez le dépôt** :
    ```sh
    git clone https://github.com/sleyzer47/toolbox.git
    cd toolbox/
    ```

2. **Installez les packages requis** :
    ```sh
    pip install -r requirements.txt
    ```

## Structure du Projet

```plaintext
toolbox/
├── main.py
├── report.pdf (si créé)
├── requirements.txt
├── result.json
├── pages/
│   ├── pdf.py
│   ├── ssh.py
│   ├── start.py
│   ├── web.py
│   ├── map.py
│   ├── menu.py
│   ├── network.py
│   ├── nmap.py
│   └── password.py
├── nikto/ (cloné depuis GitHub)
├── sqlmap-dev/ (cloné depuis GitHub)
└── wordlists/
    ├── username/
    └── password/
