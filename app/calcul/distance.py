# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 13:53:40 2016
Last Update on Wed 7 14:00:00 2016
@author: Groupe 6
Last Update author : Groupe 6
Objectif : Calculer les distances et le temps entre deux points en fonction
du traffic

Commentaire : A voir pour rassembler Parours et ListParcours
                ListParcours fonctionnne aussi pour un seul parcours.
"""


# -*- coding: utf-8 -*-
#Librairies
from app.outils import utile
import json

class Parcours:
    ''' Classe définissant un parcours :
    - départ : coordonnées du lieu de départ {"lat"= valeur , "lon" = valeur} 
        (Dictionnaire de donnée)
    - arrive : coordonnées du lieu d'arrivée {"lat"= valeur , "lon" = valeur} 
        (Dictionnaire de donnée)
    - heure_debut : heure du départ
    - distance : distance en km
    - temps : durée du trajet en minutes
    '''
    ''' !! Penser à rendre la clef secrete pour l'application finale '''
    
    def __init__(self,depart, arrivee, heure_debut, 
                     date_format = "%Y-%m-%d %H:%M:%S"):
        ''' Instantie la classe Parcours'''
        self.depart = depart
        self.arrivee = arrivee
        self.heure_debut = heure_debut
        
        # Préparation de l'URL pour l'API
        base = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
        origine = 'origins=' + str(depart["lat"]) + "," + str(depart["lon"])
        destination = '&destinations=' + str(arrivee["lat"]) + "," + str(arrivee["lon"])
        departure_time = '&departure_time=' + str(round(utile.convert_date(heure_debut,date_format)))
        fin_url = '&traffic_model=best_guess&mode=driving&language=fr-FR&key=AIzaSyCQnaoaMu6GVo3AwRzN62l0onao2TPN_u0'
    
        # Concaténation des éléments de l'URL
        url = base + origine + destination + departure_time + fin_url
        response = utile.requete_http(url)
        json_response = json.loads(response)
    
        # Récupération de la distance et du temps de parcous
        self.distance=  round(json_response['rows'][0]['elements'][0]['distance']['value'] / 1000,2)
        self.temps= round(json_response['rows'][0]['elements'][0]['duration_in_traffic']['value'] / 60,2)


class ListParcours:
    ''' Classe définissant le calcul pour une liste de parcours :
    - départ : coordonnées du lieu de départ {"lat"= valeur , "lon" = valeur} (Dictionnaire de donnée)
    - arrive : Tableau des coordonnées du lieu d'arrivée [{"lat"= valeur , "lon" = valeur}] (Tableau composé de un un ou plusieurs dictionnaires de données)
    - heure_debut : heure du départ
    - trajet : liste des trajets avec le point d'arrivée (lat, long), le temps et la distance
    '''
    ''' !! Penser à rendre la clef secrete pour l'application finale '''
    
    def __init__(self,depart, arrivee, heure_debut, date_format = "%Y-%m-%d %H:%M:%S"):
        self.depart = depart
        self.arrivee = arrivee
        self.heure_debut = heure_debut
        
        # Préparation de l'URL pour l'API
        base = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
        origine = 'origins=' + str(depart["lat"]) + "," + str(depart["lon"])
        destination = '&destinations='
        for lieu in arrivee:
            destination= destination + str(lieu["lat"]) + "," + str(lieu["lon"]) + "|"
        departure_time = '&departure_time=' + str(round(utile.convert_date(heure_debut,date_format)))
        fin_url = '&traffic_model=best_guess&mode=driving&language=fr-FR&key=AIzaSyCQnaoaMu6GVo3AwRzN62l0onao2TPN_u0'
       
       # Concaténation des éléments de l'URL
        url = base + origine + destination + departure_time + fin_url
        response = utile.requete_http(url)
        json_response = json.loads(response)
        trajet=[]
        i=0
        # Récupération des distances et des temps de parcours des trajets
        for element in json_response["rows"][0]["elements"]:
            temp = arrivee[i]
            temp["distance"] = round(element['distance']['value'] / 1000,2)
            temp["temps"] =  round(element['duration_in_traffic']['value'] / 60,2)
            trajet.append(temp)
            i=i+1
        self.trajet = trajet

