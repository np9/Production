# -*- coding: utf-8 -*-
"""
Éditeur de Spyder
Auteur : Groupe 6
Objectif : Tester la fonction qui permet d'ordonner les conducteurs LIBRES en fonction 
des stations et du nombre de places du véhicule passés en paramètre
"""


from app.calcul import conducteur_dispo_ordonnee

##Tests

def test_conducteur_dispo_ordonnee():
    '''Test de la fonction conducteur_dispo_ordonnee'''
    liste = ['Balma', 'Capitole']
    a=conducteur_dispo_ordonnee.ordonnancement(liste, 3)
    assert a == [('33659854658',), ('33656892345',)]