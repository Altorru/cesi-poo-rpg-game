# 🎮 RPG Game - Projet POO

## 📚 Contexte
Projet réalisé dans le cadre de la formation **Concepteur Développeur d'Applications** à **CESI La Rochelle**.  
Ce projet a pour objectif la mise en pratique des concepts de **Programmation Orientée Objet (POO)**.

## 🎯 Description
Jeu RPG en ligne de commande permettant de combattre des ennemis, explorer des zones et progresser en gagnant de l'expérience.

## ✨ Fonctionnalités

### Modes de jeu
- **🗺️ Mode Exploration** : Parcourez des zones avec plusieurs stages et affrontez un boss final
- **⚔️ Mode Classique** : Combats infinis jusqu'à la défaite

### Système de jeu
- Création de héros personnalisé
- Combat au tour par tour basé sur la vitesse des personnages
- Système d'expérience et de nivellement
- Inventaire d'armes et d'objets
- Sauvegarde des meilleurs scores
- Événements aléatoires en exploration (combats, trésors, pièges)

## 🛠️ Technologies utilisées
- **Python 3**
- **questionary** : Interface en ligne de commande interactive

## 🎓 Concepts POO mis en pratique
- **Encapsulation** : Propriétés et accesseurs
- **Héritage** : Classes Hero, Enemy, Boss
- **Polymorphisme** : Comportements différenciés selon les personnages
- **Design Patterns** :
  - **Factory Pattern** : `HeroFactory`, `EnemyFactory`
  - **Observer Pattern** : Notifications d'événements de jeu
- **Composition** : Systèmes d'inventaire et d'armes

## 🚀 Installation et lancement

### Prérequis
- Python 3.8+
- pip

### Installation
```bash
pip install -r requirements.txt
```

### Lancement du jeu
```bash
python main.py
```

## 📁 Structure du projet
```
├── main.py           # Point d'entrée du jeu
├── base.py           # Classes de base (Character, Hero, Enemy, Boss, Weapon)
├── exploration.py    # Système d'exploration de zones
├── factories.py      # Factory patterns pour création de personnages
├── observer.py       # Implémentation du pattern Observer
├── scores.py         # Gestion des scores
└── requirements.txt  # Dépendances Python
```

## 👨‍🎓 Auteur
VIAUD Hugo - CESI La Rochelle - 2025

---
*Développé dans le cadre du module Programmation Orientée Objet*
