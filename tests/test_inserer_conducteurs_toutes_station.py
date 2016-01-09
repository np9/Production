# -*- coding: utf-8 -*-
'''
Éditeur de Spyder
Auteur : Groupe 6
Objectif : Tester la fonction qui permet d'inserer dans la 
base de données tous les chauffeurs qui ne sont pas inactifs
(meme_station = True or meme_station = False)
'''
# C'est pas le bon chemin d'import!
from app.calcul import insertion_propositions

##Tests
def test_insertion_proposition:
    '''Test de la  fonction inserer_conducteurs_toutes_station'''
    #Ici, on compare le nombre de ligne que l'on va ajouter dans la base de données avec le nombre de ligne attendu 
    assert insertion_proposition.inserer_conducteurs_toutes_station(1,[{'telephone': '33699428430', 'station': 'Esquirol'}],'Esquirol') == 1
