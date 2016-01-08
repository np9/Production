# -*- coding: utf-8 -*-
"""
@author: Groupe 6
Objectif : Différentes fonctions permettant de récupérer des informations 
sur la course.
Last Upate : 8/01/2016 13:00
"""

from app import db
from haversine import haversine



def information_course(numero):
    ''' Récupère des informations sur la course passée en paramètre '''

    # Création de la requete de selection des conducteurs
    query = '''SELECT places, animaux, animaux_grands
            FROM  Courses
            WHERE numero = {numero_course} ;'''         

    # Création et execution de la requête parametrée
    query_param = query.format(numero_course=numero)
    result = db.engine.execute(query_param).fetchall()  
   
    # Création du dictionnare contenant les informations 
    course = {}
    course['numero']  =  numero 
    course['places']  =  result[0][0] 
    course['animaux_petit']  =  result[0][1]  
    course['animaux_gros']  =  result[0][2] 
    
    
    return course
    

def stations_proches(depart):
    ''' Fonction qui permet de trouver la station la plus proche de l'utilisateur
    Paramètres :
        depart : adresse de départ du client
    '''

    # Récupération des coordonnees (longitude et latitude) du point de départ
    position_depart = ''' SELECT distinct ST_X(A.position) AS latitude, ST_Y(A.position) AS longitude
                          FROM Adresses A
                          WHERE A.identifiant = {req_depart} '''
                          
    # Création et execution de la requête parametrée
    query_param = position_depart.format(req_depart=depart)
    result = db.engine.execute(query_param)    
    position_client=result.fetchall() 
    
    # Coordonées GPS du client
    coord_client=(position_client[0][0],position_client[0][1])
    
    # Récupération des coordonnées (longitude et latitude) de chaque station, son rayon exterieur et son nom   
    position_station = ''' SELECT distinct ST_X(A.position) AS latitude, 
                                    ST_Y(A.position) AS longitude, 
                                    distance_sortie AS rayon, S.nom
                            FROM Stations S, Adresses A
                            WHERE S.Adresse = A.identifiant; '''
            
    # Stockage des résultats de la requête            
    position_station = db.engine.execute(position_station)    
    liste_position_station=position_station.fetchall()
  
    # Pour chaque station, calculer la distance entre la station et l'utilisateur en metre
    liste_distance=[]  
    for position in liste_position_station:
        coord_station=(position[0],position[1])
        dist_centre  = haversine(coord_station,coord_client)
        dist_centre = dist_centre * 1000
        dist_bor= dist_centre - position[2]
        liste_distance.append({'station' : position[3], 'distance' : dist_bor})

    # Trier les distanes par ordre croissant et on recupere le minimum
  
    distance_minimum = min(liste_distance, key=lambda k: k['distance'])['distance']

    # On cree une boucle qui affiche toute les stations pour lesquelles la distance entre l'utilisateur et la station est minimale    
    station_proche = []   
    for i in  range(0, len(liste_distance)):  
        if ((liste_distance[i].get('distance')) == distance_minimum) or (liste_distance[i].get('distance') <= 0):
            station_proche.append({'station' : liste_distance[i].get('station')})

    return station_proche
    
    