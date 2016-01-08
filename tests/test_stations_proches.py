# -*- coding: utf-8 -*-
"""
Éditeur de Spyder
Auteur : Groupe 6
Objectif : Tester la fonction qui permet de trouver la station la plus proche de l'utilisateur
"""


from app.attribution import course
##Tests

def test_client_station_distance():
    #Test de la fonction Cd_Libre_station
    assert  course.stations_proches(2) == ['Blagnac', 'La Cepiere']
