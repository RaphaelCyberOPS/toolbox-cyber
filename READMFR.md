# toolbox-cyber par HackMeRaphaël

## Introduction

Bienvenue sur le site de Pentest Toolbox, un projet développé dans le cadre de mon master en cybersécurité.

Cet outil est conçu pour automatiser les tests de pénétration professionnels.

Il regroupe divers résultats d’analyse dans un rapport PDF bien structuré, ce qui permet aux professionnels de la sécurité d’examiner et de traiter plus facilement les vulnérabilités.

L’application a été développée en python et fonctionne sous Windows, ce qui la rend facile d’accès, pour un accès plus facile. L’application peut être utilisée sans aucune connaissance de la cybersécurité.

Cependant, l’interprétation des résultats peut être compliquée sans une telle connaissance.

## Features

### 1. Acquisition Nmap
L’outil intègre Nmap pour effectuer une analyse du réseau et recueillir des informations sur les ports ouverts, les services et les versions.
Il collecte également toutes les CVE associées (vulnérabilités et expositions communes) à l’aide du script vulners.

##2. Analyse Web
L’outil peut traiter les résultats des scanners d’applications Web, en particulier SQLMap et Nikto, fournissant des informations détaillées sur les vulnérabilités potentielles des applications Web.

- **SQLMap** : SQLMap est un outil de test d’intrusion open source qui automatise le processus de détection et d’exploitation des failles d’injection SQL et de prise en charge des serveurs de bases de données. En intégrant SQLMap, cette boîte à outils peut identifier les vulnérabilités d’injection SQL et aider à sécuriser les applications Web contre de telles attaques.
  - **Information** : The SQLMap clone project from [GitHub - SQLMap](https://github.com/sqlmapproject/sqlmap).
  
- **Nikto** : Nikto est un scanner de serveur Web open-source qui effectue des tests complets contre les serveurs Web pour plusieurs éléments, y compris plus de 6700 fichiers/CGI potentiellement dangereux, vérifie les versions obsolètes et les problèmes spécifiques aux versions. L’intégration de Nikto permet à cette boîte à outils d’identifier diverses vulnérabilités dans les serveurs Web et les applications.
  - **Information** : The Nikto clone project from [GitHub - Nikto] (https://github.com/sullo/nikto).

### 3. SSH Brute Force
Cette fonctionnalité capture et signale les résultats des attaques par force brute SSH, y compris les ports testés, les listes de noms d’utilisateur, les listes de mots de passe et les résultats des tests.
