import numpy as np
import pandas as pd
import csv
import tkinter as tk
import random

class Lieu:
    def __init__(self, x, y, nom):
        self.x = x
        self.y = y
        self.nom = nom

    def distance(self, lieu):
        return np.sqrt((self.x - lieu.x)**2+(self.y - lieu.y)**2)

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
        for i in range(NB_LIEUX):
            for j in range(i+1, NB_LIEUX):
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
            # print("Distance entre",lieu_actuel.nom," et ",lieu_suivant.nom,": ",lieu_actuel.distance(lieu_suivant))
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
    
class TSP_GA:
    def __init__(self, graph, taille_population=50, prob_croisement=0.8, prob_mutation=0.05, ratio_selection=0.7, n_meilleurs=5):
        self.population = []
        self.graph = graph
        self.taille_population = taille_population
        self.prob_croisement = prob_croisement
        self.prob_mutation = prob_mutation
        self.ratio_selection = ratio_selection
        self.n_meilleurs = n_meilleurs        

    def selection(self):
        dist = []
        for route in self.population:
            dist.append((route, self.graph.calcul_distance_route(route)))
            dist.sort(key=lambda x: x[1])
            selectionnes = [route for route, _ in dist[:int(self.ratio_selection * self.taille_population)]]
            # restants = [route for route, _ in dist[int(self.ratio_selection * self.taille_population):]]
        
        return selectionnes


    def croisement(self, parent1, parent2):
        enfants = []
        cut = np.random.randint(1, NB_LIEUX-1)
        enfant1 = Route(parent1.ordre[:cut] + [x for x in parent2.ordre if x not in parent1.ordre[:cut]] + [0])
        enfant2 = Route(parent2.ordre[:cut] + [x for x in parent1.ordre if x not in parent2.ordre[:cut]] + [0])
        
        enfants.append(enfant1)
        enfants.append(enfant2)
        return enfants

    def mutation(self, enfant):       
        villes_a_echanger = np.random.default_rng().choice(range(1, NB_LIEUX-1), size=2, replace=False)
        enfant.ordre[villes_a_echanger[0]], enfant.ordre[villes_a_echanger[1]] = enfant.ordre[villes_a_echanger[1]], enfant.ordre[villes_a_echanger[0]]
        return enfant
    
    def meilleures_routes(self):
        a = [self.graph.calcul_distance_route(route) for route in self.population]
        indexed_distances = list(enumerate(a))
        indexed_distances.sort(key=lambda x: x[1])
        # print(f"Indice de l'individu avec la plus petite distance: {best_index}")
        return  [index for index, distance in indexed_distances[:self.n_meilleurs]]


    def check_doublons(self,population):
        seen = set()
        doublons = []
        for route in population:
            route_repr = tuple(route.ordre)  # Assurez-vous que route.ordre est une séquence immuable
            if route_repr in seen:
                doublons.append(route)
            else:
                seen.add(route_repr)
        return doublons

    def remove_doublons2(self, population):
        seen = set()
        unique_population = []
        for route in population:
            route_repr = tuple(route.ordre)  # Assurez-vous que route.ordre est une séquence immuable
            if route_repr not in seen:
                seen.add(route_repr)
                unique_population.append(route)
        return unique_population

    def iteration(self,selectionnes):
        i=0
        nouvelle_population = []
        while len(nouvelle_population) < self.taille_population:
            # print(i)
            # random.shuffle(selectionnes)
            if np.random.rand() < self.prob_croisement:
                enfants = self.croisement(selectionnes[i], selectionnes[i+1])
                for enfant in enfants:
                    if np.random.rand() < self.prob_mutation:
                        enfant = self.mutation(enfant)
                    nouvelle_population.append(enfant)
            else:
                pass
                # nouvelle_population.append(selectionnes[i])
                # nouvelle_population.append(selectionnes[i+1])
            i += 2
            if i == len(selectionnes)-2:
                i = 0
        return nouvelle_population

    def execute(self):
        
        # self.population = population
        doublons = [1]
        selectionnes = self.selection()
        unique = []

        nouvelle_population = self.iteration(selectionnes)
        doublons = self.check_doublons(nouvelle_population)
        # print("Doublons avant: ",len(doublons)," sur ",len(nouvelle_population))
        population_intermediaire = [Route(None) for _ in range(len(doublons))]
        # print(len(self.check_doublons(population_intermediaire)))

        unique = self.remove_doublons2(nouvelle_population)
        unique += population_intermediaire

        nouvelle_population = unique
        doublons = self.check_doublons(nouvelle_population)
        # print("Doublons apres: ",len(doublons)," sur ",len(nouvelle_population))
        # print("Nouvelle population: ",len(nouvelle_population))
        return nouvelle_population, self.meilleures_routes()

    def run(self):

        min = np.inf
        self.population = [Route(None) for _ in range(nb_population)]
        for i in range(nb_iterations):

            while affichage.paused:
                affichage.window.update_idletasks()
                affichage.window.update()

            self.population, info_dist = self.execute()

            if graph.calcul_distance_route(self.population[info_dist[0]]) < min:
                c = 0
                min = graph.calcul_distance_route(self.population[info_dist[0]])
                min_route = self.population[info_dist[0]]
            elif(graph.calcul_distance_route(self.population[info_dist[0]]) == min):
                c += 1
            if(c==int(0.02*nb_iterations)):
                affichage.window.destroy()
                return min_route, min

            affichage.display_route(min_route, color="blue", mini=True)
            affichage.display_n_best_routes(self.population, info_dist, n_route = 5)
            affichage.update_label("Iteration: " + str(i) + " Meilleure distance trouvée : " + str(graph.calcul_distance_route(self.population[info_dist[0]]))+"Minimum all time: "+str(min))

            affichage.window.update_idletasks()
            affichage.window.update()

        affichage.run()

        return min_route, min
        # self.population = nouvelle_population


class Affichage:
    def __init__(self, graph):
        self.graph = graph
        self.window = tk.Tk()
        self.window.title("Groupe G")
        self.canvas = tk.Canvas(self.window, width=LARGEUR, height=HAUTEUR)
        self.canvas.pack()

        self.label = tk.Label(self.window, text="Informations:")
        self.label.pack()

        self.paused = False
        self.show_best_routes = False
        self.window.bind("<space>", self.toggle_pause)
        self.window.bind("<b>", self.toggle_best_routes)
        self.window.bind("<Key>", self.handle_key_press)
        self.window.bind("<Escape>", self.handle_escape)

    def toggle_best_routes(self, event):
        self.show_best_routes = not self.show_best_routes
        if not self.show_best_routes:
            self.canvas.delete("route")

    def update_label(self, text):
        self.label.config(text=text)

    def toggle_pause(self, event):
        self.paused = not self.paused

    def handle_key_press(self, event):
        self.display_n_best_routes()

    def handle_escape(self, event):
        self.window.destroy()

    def display_n_best_routes(self, population, indice, n_route=5):
        if self.show_best_routes:
            self.canvas.delete("route")
            for i in range(n_route):
                self.display_route(population[indice[i]], color="gray")

    def display_route(self, route, color, mini=False):
        if mini:
                self.canvas.delete("route_mini")
        for i in range(len(route.ordre) - 1):
            
            lieu_actuel = self.graph.liste_lieux[route.ordre[i]]
            lieu_suivant = self.graph.liste_lieux[route.ordre[i + 1]]

            if mini:
                self.canvas.create_line(lieu_actuel.x, lieu_actuel.y, lieu_suivant.x, lieu_suivant.y, fill="blue", tag="route_mini",width=5)
            else:
                self.canvas.create_line(lieu_actuel.x, lieu_actuel.y, lieu_suivant.x, lieu_suivant.y, fill=color, dash=(4, 4), tag="route")

    def run(self):
        self.window.mainloop()

# main
LARGEUR = 800
HAUTEUR = 600
graph = Graph()
NB_LIEUX = graph.generer_lieux(path='data/graph_200.csv')
graph.calcul_matrice_cout_od()
affichage = Affichage(graph)

nb_iterations = 2000
nb_population = NB_LIEUX*5
n_route = 100

solver = TSP_GA(graph, taille_population=nb_population, prob_mutation=0.2, prob_croisement=0.5, ratio_selection=0.3,n_meilleurs = n_route)
min_route, min = solver.run()
print("Meilleure route trouvée: ",min_route.ordre, "Distance: ",min)
