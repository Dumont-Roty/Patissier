from patissier.recettes import *

# Création d'une recette
ListeNomsSousProduits = ["Fraises coupées", "Pâte à tarte"," Pâte à chou", "Pâte à chou reposée", "Choux vides", "Choux à la crème",
 "Crème pâtissière", "Pâte à tarte cuite","Pâte à tarte cuite et froide","Tartes aux fraises"]

ListeSousProduits = [sousProduit(nom) for nom in ListeNomsSousProduits]

ListeEtapes = [
    etape("Couper les fraises", produitFinal=sousProduit("Fraises coupées"), duree=10),
    etape("Préparer crème patissière", produitFinal=sousProduit("Crème pâtissière"), duree=30),
    etape("Préparer la pâte à tarte", produitFinal=sousProduit("Pâte à tarte"), duree=5),
    etape("Préparer pâte à chou", produitFinal=sousProduit("Pâte à chou"), duree=15),
    etape("Cuisson pâte à tarte", produitFinal=sousProduit("Pâte à tarte cuite"), duree=45,
          besoinFour=True, etapeActive=False, sousProduitNecessaires=[sousProduit("Pâte à tarte")]),
    etape("Attendre la pâte froide", produitFinal=sousProduit("Pâte à tarte cuite et froide"), duree=30,
          etapeActive=False, sousProduitNecessaires=[sousProduit("Pâte à tarte cuite")]),
    etape("Dressage tarte aux fraises", produitFinal=sousProduit("Tartes aux fraises"), duree=10,
          etapeActive=True, sousProduitNecessaires=[sousProduit("Pâte à tarte cuite et froide"), sousProduit("Fraises coupées"), sousProduit("Crème pâtissière")]),

    etape("Faire reposer pâte chou", produitFinal=sousProduit("Pâte à chou reposée"), duree = 60,
                    etapeActive = False, sousProduitNecessaires=[sousProduit("Pâte à chou")]),
    etape("Cuisson choux", produitFinal=sousProduit("Choux vides"), duree = 25,
                    besoinFour = True, etapeActive = False, sousProduitNecessaires=[sousProduit("Pâte à chou reposée")]),
    etape("Dressage choux", produitFinal=sousProduit("Choux à la crème"), duree = 20,
                    sousProduitNecessaires=[sousProduit("Choux vides"), sousProduit("Crème patissière")])
]
