# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 13:53:40 2016
Last Update on Wed 6 12:00:00 2016
@author: Groupe 6
Last Update author : Groupe 6
Objectif : Calculer les distances et le temps entre deux points en fonction
du traffic
"""


# -*- coding: utf-8 -*-
#Librairies
from app.outils import utile
import json

def parcours(depart, arrivee, heure_debut):
    '''Fonction permettant de formater l'url et de calculer les distances
    Attention à la key qu'il faudra changer'''
    base = 'https://maps.googleapis.com/maps/api/directions/json?'
    origine = 'origin=' + utile.formatage_url(depart)
    destination = '&destination=' + utile.formatage_url(arrivee)
    departure_time = '&departure_time=' + str(round(utile.convert_date(heure_debut)))
    fin_url = '&traffic_model=pessimistic&mode=driving&language=fr-FR&key=AIzaSyCQnaoaMu6GVo3AwRzN62l0onao2TPN_u0'
    
    '''Ajouter l'heure de depart à l'url'''
    url = base + origine + destination + departure_time + fin_url
    reponse = utile.requete_http(url)
    return json.loads(reponse)


def get_distance(json):
    '''Fonction permettant de récupérer la distance entre deux points'''
    resultat = json['routes'][0]['legs'][0]['distance']['value']
    resultat = round(resultat / 1000,2)
    return resultat

       
def get_heure(json):
    '''Fonction permettant de récuperer le temps de parcours entre deux points'''
    resultat = json['routes'][0]['legs'][0]['duration_in_traffic']['value']
    resultat = round(resultat / 60)
    return resultat

