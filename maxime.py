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
NB_LIEUX = 5

class Graph:
    def __init__(self):
        self.liste_lieux = []
        self.matrice_od = None

    def generer_lieux(self):
        # read csv
        # it has this form : first line is x,y 
        with open('data/graph_5.csv', 'r') as file:
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
graph.generer_lieux()
graph.calcul_matrice_cout_od()
print((graph.matrice_od))

#test du plus proche voisin
lieu = graph.liste_lieux[1]
plus_proche = graph.plus_proche_voisin(lieu)
print("Le lieu: ",lieu.nom," a pour voisin le plus proche: ",plus_proche.nom)

# calcul la total distance
route = Route([0, 3 ,1 ,4 ,2, 0])
print("Distance total:", graph.calcul_distance_route(route))

#test affichage
#affichage = Affichage(graph)
#affichage.display_route(route)
#affichage.run()






