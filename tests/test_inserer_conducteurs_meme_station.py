# -*- coding: utf-8 -*-
"""
Éditeur de Spyder
Auteur : Groupe 6
Objectif : Tester la fonction qui permet d'inserer dans la 
base de données tous les chauffeurs qui ne sont pas inactifs
(meme_station = True or meme_station = False)
"""

from app.calcul import insertion_propositions

##Tests
def test_insert_proposition():
    '''Test de la  fonction inserer_conducteurs_meme_station'''
    #Ici, on compare le nombre de ligne que l'on va ajouter dans la base de données avec le nombre de ligne attendu 
    assert insertion_propositions.inserer_conducteurs_meme_station(1,['33699428430','33624421417'],'Esquirol') == 2
