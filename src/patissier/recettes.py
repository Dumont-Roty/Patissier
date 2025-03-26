from typing import List
from graphlib import *

class sousProduit(object):

    def __init__(self, nom :str):
        self.nom : str = nom

    def __eq__(self, autre):
        return self.nom == autre.nom
    
    def __hash__(self):
        return hash(self.nom)

class etape(object):
    # si peut de chose dans le init alors plus simple
    # Paramètres optionnels UNIQUEMENT A LA FIN
    def __init__(self, nomEtape : str,produitFinal:sousProduit, duree : int, 
                 sousProduitNecessaires: List[sousProduit] = [],
                 besoinFour : bool=False, etapeActive : bool=True):
        self.nom = nomEtape
        self.besoinFour : bool = besoinFour
        self.duree : int = duree
        self.active : bool = etapeActive
        self.sousProduitFinal : sousProduit = produitFinal
        self.sousProduitNecessaires : List[sousProduit] = sousProduitNecessaires
        
    def __eq__(self, autre):
        if self.sousProduitFinal == autre.sousProduitFinal and self.sousProduitNecessaires == autre.sousProduitNecessaires:
            return True
        return False
                
        
class recette(object):
    def __init__(self, listeEtapes : list[etape]):
        self.listeEtapes : list[etape] = listeEtapes
        
        self.listesousProduits : list[sousProduit] = []
        for step in self.listeEtapes:
            if step.sousProduitFinal not in self.listesousProduits:
                self.listesousProduits.append(step.sousProduitFinal)
                
    def verifierValide(self):
        """_summary_
        Vérifie si les sous produits necessaires pour la recette peuve,t etre obtnue via une étape de la recette.
        
        Paremètre :
        - Aucun
        
        Renvoie : 
        - booléen : Vrai si la recette est auto-suffisante, faux sinon
        """
        listePrerequis = []
        for step in self.listeEtapes:
            for prerequis in step.sousProduitNecessaires:
                if prerequis not in self.listesousProduits:
                    return False
        return True 
    
    
class planing(object):
    
    def __init__(self, listeRecette : str):
        self.listeRecette : list[recette] = listeRecette
        
        self.listeSousProduit = []
        for recipe in self.listeRecette:
            self.listeSousProduit += [ prod for prod in recipe.listesousProduits if prod not in self.listeSousProduit ]
        
        self.listeEtape = []
        for recipe in self.listeRecette:
            self.listeEtape += [ step for step in recipe.listeEtapes if step not in self.listeEtape]
            
        self.planning : List[etape] = []
            
    def genererPlaning(self):
        
        graph =  dict()
        for sousProduit in self.listeSousProduit:
            L = []
            for step in self.listeEtape:
                    if( step.sousProduitFinal == sousProduit ):
                        L += [ produits for produits in step.sousProduitNecessaires if produits not in L ]
                        # Ajout de l'intégralité des prédécésseur d'un sous produit sans avoir de doublon # CONCATENE les listes
                        # L.append(step.sousProduitNecessaires) ===> [1,2,[3,4]]
            graph[sousProduit] = list(L) #Obtention des prédécésseur d'un sous produit en créant une copie de la liste
        ts = TopologicalSorter(graph)
        triTopo = list(ts.static_order())
        self.planning = []
        for prod in triTopo:
            for step in self.listeEtape:
                if step.sousProduitFinal == prod:
                    self.planning.append(step)
            
    def __str__(self):
        S = "Ordre possible : \n"
        temps = 0
        for i, step in enumerate(self.planning):
            S += str(i+1) + ") " + step.nom + ", durée : " + str(step.duree) + " min\n"
            temps += step.duree
        S += "Temps total : " + str(temps) + " min"
        return S 