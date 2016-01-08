# -*- coding: utf-8 -*-
"""
Éditeur de Spyder
Auteur : Groupe 6
Objectif : Tester la fonction qui convertit la date rentrée en paramètre en timestamp (sec depuis 19790)
"""

from app.outils import utile

##Tests


def test_convert_date(self):
    '''Test de la fonction convert_date'''
    date="2016-07-01 19:30:00"
    assert utile.convert_date(date, date_format = "%Y-%m-%d %H:%M:%S") == 1467394200.0

    