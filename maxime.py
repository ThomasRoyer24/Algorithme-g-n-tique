import numpy as np
import pandas as pd
import csv
import tkinter as tk

class Lieu:
    def __init__(self, x, y, nom):
        self.x = x
        self.y = y
        self.nom = nom

    def distance(self, lieu):
        return np.sqrt((self.x - lieu.x)**2+(self.y - lieu.y)**2)

LARGEUR = 800
HAUTEUR = 600
#NB_LIEUX = 5

class Graph:
    def __init__(self):
        self.liste_lieux = []
        self.matrice_od = None

    def generer_lieux(self,path):
        print("Lieux: ")
        # it has this form : first line is x,y 
        with open(path, 'r') as file:
            reader = csv.reader(file) # pas la premiere ligne
            next(reader)
            count = 0
            for row in reader:
                print(row)
                x = float(row[0])
                y = float(row[1])
                lieu = Lieu(x, y, "nom"+str(count))
                count +=1
                self.liste_lieux.append(lieu)
        return count

    def calcul_matrice_cout_od(self):

        # optimiser car on calcule 2 fois la meme distance
        self.matrice_od = np.zeros((NB_LIEUX, NB_LIEUX))
        dictionnaire = {}
        for i in range(NB_LIEUX):
            for j in range(i, NB_LIEUX):
                dist_ij = self.liste_lieux[i].distance(self.liste_lieux[j])
                self.matrice_od[i, j] = dist_ij                

    def plus_proche_voisin(self, lieu):
        index = self.liste_lieux.index(lieu)
        ligne = self.matrice_od[index]
        index_min = np.argmin(ligne)
        return self.liste_lieux[index_min]

    def calcul_distance_route(self, route):
        distance_totale = 0
        for i in range(len(route.ordre)-1):
            lieu_actuel = self.liste_lieux[route.ordre[i]]
            lieu_suivant = self.liste_lieux[route.ordre[i+1]]
            distance_totale += lieu_actuel.distance(lieu_suivant)
            print("Distance entre",lieu_actuel.nom," et ",lieu_suivant.nom,": ",lieu_actuel.distance(lieu_suivant))
        return distance_totale
    
class Route:
    def __init__(self, ordre):
        if ordre is None:
            self.ordre = np.random.permutation(range(1, NB_LIEUX)) # ou sample ou shuffle
            # ajouter 0 en première et dernière position
            self.ordre = np.insert(self.ordre, 0, 0)
            self.ordre = np.append(self.ordre, 0)
            self.ordre = self.ordre.tolist()
        else:
            if ordre[0] != 0 or ordre[-1] != 0:
                raise ValueError("L'ordre doit commencer et finir par 0")
            # faire une copy plutot
            self.ordre = ordre[:]
    

class Affichage:
    def __init__(self, graph):
        self.graph = graph
        self.window = tk.Tk()
        self.window.title("Groupe G")
        self.canvas = tk.Canvas(self.window, width=LARGEUR, height=HAUTEUR)
        self.canvas.pack()
        self.text = tk.Text(self.window)
        self.text.pack()

        self.window.bind("<Key>", self.handle_key_press)
        self.window.bind("<Escape>", self.handle_escape)

    def handle_key_press(self, event):
        if event.char == "N":
            self.display_n_best_routes()
        elif event.char == "M":
            self.display_cost_matrix()

    def handle_escape(self, event):
        self.window.destroy()

    def display_n_best_routes(self, n=5):
        print("Test N")
        best_routes = self.graph.find_n_best_routes(n)
        for route in best_routes:
            self.display_route(route, color="light gray")

    def display_cost_matrix(self):
        cost_matrix = self.graph.get_cost_matrix()
        self.text.insert(tk.END, str(cost_matrix))

    def display_route(self, route, color="blue"):
        for i in range(len(route.ordre) - 1):
            lieu_actuel = self.graph.liste_lieux[route.ordre[i]]
            lieu_suivant = self.graph.liste_lieux[route.ordre[i + 1]]
            self.canvas.create_line(lieu_actuel.x, lieu_actuel.y, lieu_suivant.x, lieu_suivant.y, fill=color, dash=(4, 4))
            self.canvas.create_text(lieu_actuel.x, lieu_actuel.y, text=str(i), fill=color)

    def run(self):
        self.window.mainloop()


#test
graph = Graph()
NB_LIEUX = graph.generer_lieux(path='data/graph_5.csv')
print("NB_lieux : ",NB_LIEUX)
graph.calcul_matrice_cout_od()
print("Matrice od : \n",graph.matrice_od)

#test du plus proche voisin
lieu = graph.liste_lieux[1]
plus_proche = graph.plus_proche_voisin(lieu)
print("Le lieu: ",lieu.nom," a pour voisin le plus proche: ",plus_proche.nom)

# calcul la total distance
route = Route([0, 3 ,1 ,4 ,2, 0])
print("Distance total:", graph.calcul_distance_route(route))

#test affichage
affichage = Affichage(graph)
best_route = Route(None)
print(best_route.ordre)
print("Distance total:", graph.calcul_distance_route(best_route))
best_route = Route(None)
print(best_route.ordre)
print("Distance total:", graph.calcul_distance_route(best_route))
best_route = Route(None)
print(best_route.ordre)
print("Distance total:", graph.calcul_distance_route(best_route))
best_route = Route(None)
print(best_route.ordre)
print("Distance total:", graph.calcul_distance_route(best_route))
affichage.display_route(best_route)
affichage.run()



class TSP_GA:
    def __init__(self):
        self.population = []
        self.graph = Graph()
        self.graph.generer_lieux()
        self.graph.calcul_matrice_cout_od()
        self.taille_population = 5
        self.nb_generations = 10000
        self.prob_croisement = 0.8
        self.prob_mutation = 0.05
        self.ratio_selection = 0.7

    def initialiser_population(self):
        for _ in range(self.taille_population):
            route = Route(None)
            self.population.append(route)
        print("Population initiale: ",self.population)


    def selection(self):
        # selection proportionnelle à l'adaptation
        distances = []
        total_distance = 0
        for route in self.population:
            distance = self.graph.calcul_distance_route(route)
            distances.append(distance)
            total_distance += distance
        probas = [distance/total_distance for distance in distances]
        return np.random.choice(self.population, int(self.ratio_selection*self.taille_population), p=probas).tolist()

    def croisement(self, selectionnes):
        enfants = []
        for i in range(0, len(selectionnes)-1, 2):
            parent1 = selectionnes[i]
            parent2 = selectionnes[i+1]
            cut = np.random.randint(1, NB_LIEUX-1)

            enfant1 = Route(parent1.ordre[:cut] + [x for x in parent2.ordre if x not in parent1.ordre[:cut]] + [0])
            enfant2 = Route(parent2.ordre[:cut] + [x for x in parent1.ordre if x not in parent2.ordre[:cut]] + [0])
            enfants.append(enfant1)
            enfants.append(enfant2)
        return enfants

    def mutation(self, enfants):
        enfants_mutes = []
        for enfant in enfants:
            if np.random.rand() < self.prob_mutation:
                villes_a_echanger = np.random.default_rng().choice(range(1, NB_LIEUX-1), size=2, replace=False)
                enfant.ordre[villes_a_echanger[0]], enfant.ordre[villes_a_echanger[1]] = enfant.ordre[villes_a_echanger[1]], enfant.ordre[villes_a_echanger[0]]
                enfants_mutes.append(enfant)
        return enfants_mutes
    
    def evaluate(self):
        best = np.inf
        for individu in self.population:
            if self.graph.calcul_distance_route(individu) < best:
                best = self.graph.calcul_distance_route(individu)
        print("Meilleure distance: ",best)

    def run(self):
        self.initialiser_population()
        self.evaluate()
        print("-----")
        for i in range(self.nb_generations):
            selectionnes = self.selection()
            enfants = self.croisement(selectionnes)
            enfants_mutes = self.mutation(enfants)
            best_individuals = sorted(self.population, key=lambda x: self.graph.calcul_distance_route(x))[:int(self.ratio_selection * self.taille_population)]
            new_individuals = selectionnes + enfants_mutes
            self.population = best_individuals + new_individuals[:len(self.population) - len(best_individuals)]

        self.evaluate()
            

solver = TSP_GA()
solver.run()





