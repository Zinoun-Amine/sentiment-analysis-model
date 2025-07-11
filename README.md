# Analyse de Sentiments des Avis TikTok 

## Vue d'ensemble du projet

Ce projet est une application web **Angular** conçue pour analyser les sentiments (Positif, Négatif, Neutre) des avis d'utilisateurs de l'application TikTok. L'application intègre un modèle de Machine Learning entraîné sur près de 300 000 avis, une API backend robuste, et une interface utilisateur dynamique et interactive.

L'objectif était de maîtriser l'ensemble du cycle de vie d'un projet de data science : de la collecte et du nettoyage des données, à l'entraînement et l'évaluation rigoureuse de modèles, jusqu'au déploiement dans une application web fonctionnelle.

###  Fonctionnalités clés

*   **Analyse en Temps Réel :** Entrez n'importe quel texte pour obtenir une prédiction de sentiment instantanée.
*   **Interface Dynamique :** La carte de résultat change de couleur et d'icône en fonction du sentiment prédit (vert pour positif, rouge pour négatif, gris pour neutre).
*   **Tableau de Bord Interactif :** Visualisez une analyse sur un échantillon aléatoire de 100 commentaires de la base de données.
*   **Expérience Utilisateur Soignée :** Animations fluides, états de chargement clairs, et design responsive.

##  Stack Technique

Ce projet combine des technologies de pointe pour le frontend, le backend et le machine learning.

*   **Frontend :**
    *   ![Angular](https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white) - Framework principal pour l'interface utilisateur.
    *   ![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white) - Pour un code robuste et typé.
    *   ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) & ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white) - Pour la structure et le style.

*   **Backend :**
    *   ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) - Framework API Python haute performance.
    *   ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) - Langage principal pour le backend et le ML.

*   **Machine Learning :**
    *   ![Scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white) - Pour le pipeline de modélisation (TF-IDF, Pipeline).
    *   **LightGBM** - Modèle de Gradient Boosting puissant pour la classification.
    *   **Imbalanced-learn** - Pour gérer le déséquilibre des classes via le sous-échantillonnage (Undersampling).
    *   ![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white) - Pour la manipulation et le nettoyage des données.


