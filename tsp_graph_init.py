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
        dictionnaire = {}
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
    def __init__(self, graph, taille_population=50, prob_croisement=0.8, prob_mutation=0.05, ratio_selection=0.7):
        self.population = []
        self.graph = graph
        self.taille_population = taille_population
        self.prob_croisement = prob_croisement
        self.prob_mutation = prob_mutation
        self.ratio_selection = ratio_selection

    def selection(self):
        # selection proportionnelle à l'adaptation
        # distances = []
        # for route in self.population:
        #     distance = self.graph.calcul_distance_route(route)
        #     distances.append(distance)
        # # probas = [distance/total_distance for distance in distances]
        # probas = [1 / distance for distance in distances]
        # total_prob = sum(probas)
        # probas = [p / total_prob for p in probas]
        # return np.random.choice(self.population, int(self.ratio_selection*self.taille_population), p=probas).tolist()

        # selection par tournoi
        # selectionnes = []
        # for _ in range(int(self.ratio_selection * self.taille_population)):
        #     tournoi = np.random.choice(self.population, 3)  # Sélection de 3 individus
        #     meilleur_individu = min(tournoi, key=lambda x: self.graph.calcul_distance_route(x))
        #     selectionnes.append(meilleur_individu)
        # return selectionnes
        dist = []
        for route in self.population:
            dist.append((route, self.graph.calcul_distance_route(route)))
        dist.sort(key=lambda x: x[1])
        # print('Test',dist)
        selected_routes = [route for route, _ in dist[:int(self.ratio_selection * self.taille_population)]]
        # for route in selected_routes:
            # print('Selected routes',route.ordre, self.graph.calcul_distance_route(route))
        return selected_routes


    def croisement(self, parent1, parent2):
        enfants = []
        cut = np.random.randint(1, NB_LIEUX-1)
        enfant1 = Route(parent1.ordre[:cut] + [x for x in parent2.ordre if x not in parent1.ordre[:cut]] + [0])
        enfant2 = Route(parent2.ordre[:cut] + [x for x in parent1.ordre if x not in parent2.ordre[:cut]] + [0])
        
        enfants.append(enfant1)
        enfants.append(enfant2)
        # print("P1 : ",parent1.ordre,sum(parent1.ordre),graph.calcul_distance_route(parent1))
        # print("P2 : ",parent2.ordre,sum(parent2.ordre),graph.calcul_distance_route(parent2))
        # print("E1 : ",enfant1.ordre,sum(enfant1.ordre),graph.calcul_distance_route(enfant1))
        # print("E2 : ",enfant2.ordre,sum(enfant2.ordre),graph.calcul_distance_route(enfant2))
        return enfants

    def mutation(self, enfant):       
        villes_a_echanger = np.random.default_rng().choice(range(1, NB_LIEUX-1), size=2, replace=False)
        enfant.ordre[villes_a_echanger[0]], enfant.ordre[villes_a_echanger[1]] = enfant.ordre[villes_a_echanger[1]], enfant.ordre[villes_a_echanger[0]]
        return enfant
    
    def test(self):
        a = [self.graph.calcul_distance_route(route) for route in self.population]
        # print(a)
        best_index = np.argmin(a)
        # print(f"Indice de l'individu avec la plus petite distance: {best_index}")
        return best_index

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

    def test2(self,selectionnes):
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
            # print("Nouvelle population: ",len(nouvelle_population))
            i += 2
            if i == len(selectionnes)-2:
                i = 0
        return nouvelle_population

    def run(self,population):

        self.population = population
        dist = []
        doublons = [1]

        for route in self.population:
            dist.append((route, self.graph.calcul_distance_route(route)))
            dist.sort(key=lambda x: x[1])
            selectionnes = [route for route, _ in dist[:int(self.ratio_selection * self.taille_population)]]
            # restants = [route for route, _ in dist[int(self.ratio_selection * self.taille_population):]]
        
        # while(len(doublons)>0):
        nouvelle_population = self.test2(selectionnes)
        doublons = self.check_doublons(nouvelle_population)
        print("Doublons: ",len(doublons)," sur ",len(nouvelle_population))

        # print("Selectionnes: ",len(selectionnes))
        # print("Restants: ",len(restants))
        # for j in range(0, len(selectionnes)-1, 2):
        #     if np.random.rand() < self.prob_croisement:
        #         enfants = self.croisement(selectionnes[j], selectionnes[j+1])
        #         for enfant in enfants:
        #             if np.random.rand() < self.prob_mutation:
        #                 enfant = self.mutation(enfant)
        #             nouvelle_population.append(enfant)
        #     else:
        #         nouvelle_population.append(selectionnes[j])
        #         nouvelle_population.append(selectionnes[j+1])
        # print(len(nouvelle_population))

        # for reste in restants:
        #     nouvelle_population.append(reste)

        # doublons = self.check_doublons(population)
        # print("Doublons: ",len(doublons)," sur ",len(population))

        self.population = nouvelle_population
        # print("Population: ",len(self.population))
        return self.population, self.test()


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
        #self.text = tk.Text(self.window)
        #self.text.pack()

    def toggle_pause(self, event):
        self.paused = not self.paused

    def handle_key_press(self, event):
        # if event.char == "N":
        self.display_n_best_routes()

    def handle_escape(self, event):
        self.window.destroy()

    def display_n_best_routes(self, population, n=5):
        if self.show_best_routes:
            self.canvas.delete("route")
            for route in population:
                self.display_route(route, color="gray")

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
            #self.canvas.create_text(lieu_actuel.x, lieu_actuel.y, text=str(i), fill=color, tag="route")

    def run(self):
        self.window.mainloop()

# main
LARGEUR = 800
HAUTEUR = 600
graph = Graph()
NB_LIEUX = graph.generer_lieux(path='data/graph_5.csv')
graph.calcul_matrice_cout_od()
affichage = Affichage(graph)
nb_iterations = 2000

nb_population = 1000

population = [Route(None) for _ in range(nb_population)]
# check doublons dans la population



solver = TSP_GA(graph, taille_population=nb_population, prob_mutation=0.5, prob_croisement=0.5, ratio_selection=0.4)
min = np.inf
for i in range(nb_iterations):

    while affichage.paused:
        affichage.window.update_idletasks()
        affichage.window.update()

    population, info_dist = solver.run(population)
    # print(info_dist)

    if graph.calcul_distance_route(population[info_dist]) < min:
        min = graph.calcul_distance_route(population[info_dist])
        min_route = population[info_dist]
        # print("Nouveau minimum: ",min)
    affichage.display_route(route=population[info_dist], color="blue", mini=True)
    affichage.display_n_best_routes(population)
    affichage.update_label("Iteration: " + str(i) + " Meilleur distance trouvée : " + str(graph.calcul_distance_route(population[info_dist]))+"Minimum: "+str(min))

    affichage.window.update_idletasks()
    affichage.window.update()

affichage.run()