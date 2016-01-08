# -*- coding: utf-8 -*-
"""
@author: Groupe 6
Objectif : Différentes fonctions permettant de lister le conducteurs
            disponibles selon des critères choisis.
Last Upate : 8/01/2016 11:00
"""

from app import db
from app.attribution import  utiles

def conducteurs_stations_disp(liste_stations, places, animaux =False, gros_animaux=False):
    ''' Liste tous les conducteurs disponibles (staut=libre) dans la ou les 
    stations proches de la course, respectant différents critères.
    Les conducteurs sont triés par ordre d'arrivé dans la station.
    Paramètres :
        liste_stations : Liste contenant des noms de station.
        places : Nombre de passagers minimum
        animaux : Defaut = false
        gros_animaux : Défaut = false
    Sorties :
        Retourne la liste des conducteurs disponibles dans la (les) station(s) 
        placée(s) en paramètre
    '''
    
    # Vérifie que la liste des stations n'est pas vide.
    if len(liste_stations) < 1 : return []
   
    # Création de la requete de selection des conducteurs
    query = '''SELECT C.telephone
                FROM vehicules V, conducteurs C
                WHERE V.conducteur = C.telephone
                    AND lower(C.statut) = lower('libre')
                    AND V.places >= {places_query}
                    AND lower(C.station) IN {station} '''
                    # Prendre en compte les pénalités + les animaux
    query = query + ''' ORDER BY C.station_entree; '''
   
    # Formate la liste des stations pour la clause IN
    liste_stations_format=utiles.formater_in_clause(liste_stations)
    
    # Création et execution de la requête parametrée
    query_param = query.format(station=liste_stations_format, places_query=places)
    result = db.engine.execute(query_param)   
    results=[]
    
    # Ajout des résultats dans une liste
    for row in result: 
        results.append(row['telephone'])
    
    return results
    

def conducteurs_tous_disp(places, animaux = False, gros_animaux=False):
    ''' Liste tous les conducteurs disponibles (statut=libre|occupé) 
    dans la ou les stations proches de la course, respectant différents critères.
    Paramètres :
        liste_stations : Liste contenant des noms de station.
        places : Nombre de passagers minimum
        animaux : Defaut = false
        gros_animaux : Défaut = false
    Sorties :
        Retourne la liste des conducteurs disponibles dans les 
        différentes stations [[{'telephone' : num , 'station': nom}]
    '''
    
    # Création de la requete de selection des conducteurs
    query = ''' SELECT telephone, station
                FROM conducteurs C, Vehicules V
                WHERE C.telephone = V.conducteur
                        AND V.places >= {places_query}
                        AND lower(statut) in (lower('libre'), lower('occupé')) 
            '''
                    # Prendre en compte les pénalités + les animaux
    query = query + ";"
    
    # Création et execution de la requête parametrée
    query_param = query.format(places_query=places)
    result = db.engine.execute(query_param)   
    results=[]
    
    
    # Ajout des résultats dans une liste
    for row in result: 
        results.append({'telephone' : str(row['telephone']), 'station':str(row['station'])})

    return results
    