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
    
class etapeTemporelle(object):
    
    def __init__(self, Etape : etape, tps_debut : int):
        self.etape = Etape
        self.tps_debut = tps_debut
        self.tps_fin = tps_debut + Etape.duree
      
  
class planing(object):
    
    def __init__(self, listeRecette : str):
        self.listeRecette : list[recette] = listeRecette
        
        self.listeSousProduit = []
        for recipe in self.listeRecette:
            self.listeSousProduit += [ prod for prod in recipe.listesousProduits if prod not in self.listeSousProduit ]
        
        self.listeEtape = []
        for recipe in self.listeRecette:
            self.listeEtape += [ step for step in recipe.listeEtapes if step not in self.listeEtape]
            
        self.planning : List[List[etapeTemporelle]] = []
            
    def genererPlaning(self, nb_commis = 1, nb_four = 1):
        
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
        
        
        self.planning = [[],[]] + [[] for _ in range(nb_commis)]
        """
        [0] -> Ligne four
        [1] -> Attente
        [2] -> Commis numéro 1
        [3] -> Commis numéro 2
        ...
        """
        tempsActuel = 0
        for prod in triTopo:
            for step in self.listeEtape:
                if step.sousProduitFinal == prod:
                    
                    # test prérequis satisfaits
                    for prerequis in step.sousProduitNecessaires:
                        for ligne2 in self.planning:
                            for etapeEnCours in ligne2:
                                if prerequis == etapeEnCours.etape.sousProduitFinal:
                                    if( etapeEnCours.tps_fin>tempsActuel):
                                        tempsActuel = etapeEnCours.tps_fin
                    if step.besoinFour:                    
                        # test si four disponible 
                        if len(self.planning[0]) != 0:
                            if(self.planning[0][-1].tps_fin > tempsActuel): #[-1] renvoie le dernier élément de la liste (ici étape dans le four)
                                tempsActuel = self.planning[0][-1].tps_fin
                                
                        
                        etapeTempo = etapeTemporelle(step, tps_debut = tempsActuel)
                        self.planning[0].append(etapeTempo)
                    elif not step.active:
                        etapeTempo = etapeTemporelle(step, tps_debut = tempsActuel)
                        self.planning[1].append(etapeTempo)
                    else:
                        if len(self.planning[2]) != 0:
                            if(self.planning[2][-1].tps_fin > tempsActuel): #[-1] renvoie le dernier élément de la liste (ici étape dans le four)
                                tempsActuel = self.planning[2][-1].tps_fin
                        etapeTempo = etapeTemporelle(step, tps_debut = tempsActuel)
                        self.planning[2].append(etapeTempo)
            
    def __str__(self):
        S = "Ordre possible : \n"
        maxTemps = 0
        for ligne in self.planning:   
            temps = 0  
            for i, step in enumerate(ligne):
                S += "[ " + str(step.tps_debut) + " - " + str(step.etape.nom) +" - " + str(step.tps_fin) + " ]"
                temps += step.etape.duree
            S += "\n"
            if(ligne[-1].tps_fin > maxTemps):
                maxTemps = ligne[-1].tps_fin
        S += "Temps total : " + str(maxTemps) + " min"
        return S