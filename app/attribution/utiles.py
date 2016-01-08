# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 23:56:30 2016

@author: etudiant
"""

def formater_in_clause(liste):
    '''cette fonction permet de formater le liste des chauffeurs disponibles 
     de la (ou de les) station(s) sélectionné(s),'''
    liste_formate = '('
    first = True
    #parcourire le liste des chauffeurs disponibles dans une station 
    for element in liste:
        if first:
            first = False
        else:
             liste_formate=liste_formate + ", "
        liste_formate=liste_formate + "lower('" + element + "')"
                
    liste_formate = liste_formate + ')'
    
    return liste_formate