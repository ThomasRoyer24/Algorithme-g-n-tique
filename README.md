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
git clone https://github.com/ThomasRoyer24/Algorithme-g-n-tique.git
cd tsp-solver
```

### 📦 Installation des dépendances
```bash
pip install -r requirements.txt
```

---

## 🚀 Utilisation
Lancer l'algorithme avec un jeu de données :
```bash
python main.py --input data/clients.json --algo genetic
```
Options disponibles pour `--algo` :
- `bruteforce` → Résolution exacte (⚠️ très lent pour `n > 10`)
- `heuristic` → Approche heuristique rapide
- `ant_colony` → Colonies de fourmis 🐜
- `genetic` → Algorithme génétique 🧬
- `simulated_annealing` → Recuit simulé 🔥

---

## 📊 Résultats & Performances
Le projet propose des visualisations des chemins optimaux avec Matplotlib et NetworkX. Les résultats peuvent être enregistrés sous forme de fichiers JSON ou affichés en temps réel.

---

## 🛠 Améliorations Futures
- 🚀 Implémentation d'une **interface web interactive**.
- 📡 Intégration d'une API FastAPI pour interagir avec le solveur.
- ⚡ Optimisation des performances pour les grands ensembles de données.

---

## 🤝 Contribuer
Les contributions sont les bienvenues ! Ouvrez une **issue** ou proposez une **pull request**. 🛠

---

## 📜 Licence
Ce projet est sous licence MIT. Voir `LICENSE` pour plus d’informations.

---

## 📞 Contact
💡 Un problème ou une suggestion ? Contacte-moi via GitHub ou en ouvrant une issue ! 🚀

