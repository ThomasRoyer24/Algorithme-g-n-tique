# 🚀 Problème du Voyageur de Commerce

## 📌 Description
Ce projet traite du **problème du voyageur de commerce** (TSP - Traveling Salesman Problem), un classique de l'optimisation combinatoire. L'objectif est de trouver le **chemin le plus court** permettant de :

1. Partir d'un **point de départ** (base logistique).
2. Visiter une série de **clients** sans repasser deux fois par le même endroit.
3. Retourner à la base logistique.

Le défi principal réside dans l'explosion combinatoire des chemins possibles (**O(n!)**), rendant la résolution exacte rapidement inapplicable pour un grand nombre de clients.

---

## 🧠 Approches Utilisées
Plutôt que de tester toutes les combinaisons possibles, nous utilisons différentes techniques pour tendre vers la meilleure solution possible :

### 🔹 **Méthodes Classiques**
- Algorithme de **plus courts chemins** pour simplifier le graphe des connexions.
- Recherche de **cycles optimaux** dans le graphe réduit.

### 🔹 **Méthodes Approximatives & IA**
- **Heuristiques** pour obtenir rapidement des solutions acceptables.
- Algorithmes inspirés de la nature :
  - 🐜 **Colonies de fourmis** (Ant Colony Optimization)
  - 🧬 **Algorithmes génétiques**
  - 🔥 **Recuit simulé** (Simulated Annealing)

---

## 📦 Installation
### 🔧 Prérequis
- Python 3.x
- Bibliothèques nécessaires (voir `requirements.txt`)

### 📥 Clonage du projet
```bash
git clone https://github.com/ton-repo/tsp-solver.git
cd tsp-solver
```
