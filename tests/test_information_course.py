# -*- coding: utf-8 -*-
"""
Éditeur de Spyder
Auteur : Groupe 6
Objectif : Tester la fonction qui permet de recuperer les informations des utilisateurs
"""


from app.attribution import course
##Tests

def test_info_client():
    #Test de la fonction info_course
    assert  course.information_course(2) == {'numero': 2, 'animaux_petit': None, 'animaux_gros': None, 'nb_place': 2}
