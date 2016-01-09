import json
from app.outils import utile


class Parcours:
    '''
    - depart : coordonnées du lieu de départ {"lat"= valeur , "lon" = valeur}
    - arrivee : coordonnées du lieu d'arrivée {"lat"= valeur , "lon" = valeur}
    - debut : heure du départ
    '''
    
    def __init__(self, depart, arrivee, debut):
        self.depart = depart
        self.arrivee = arrivee
        self.debut = debut
        self.base = 'https://maps.googleapis.com/maps/api/distancematrix/json'
        self.parametres = '&traffic_model=best_guess&mode=driving&language=fr-FR'
        self.cle = 'key=AIzaSyCQnaoaMu6GVo3AwRzN62l0onao2TPN_u0'

    def construire(self):
        ''' Préparation de l'URL pour l'API. '''
        origine = 'origins={0},{1}'.format(self.depart['lat'], self.depart['lon'])
        destination = 'destinations={0},{1}'.format(self.arrivee['lat'], self.arrivee['lon'])
        depart = 'departure_time={0}'.format(int(self.debut.timestamp()))
        self.url = '{0}?{1}&{2}&{3}&{4}&{5}'.format(self.base, origine, destination, depart,
                                                    self.parametres, self.cle)
    
    def calculer(self):
        '''
        Calculer la durée et la distance d'un parcours
        à partir d'une URL.
        '''
        # Construire l'URL de trajet
        self.construire()
        # Requêter l'URL
        reponse = utile.requete_http(self.url)
        informations = json.loads(reponse)
        # Extraction de la distance
        self.distance = informations['rows'][0]['elements'][0]['distance']['value']
        # Extraction de la durée
        self.duree = informations['rows'][0]['elements'][0]['duration_in_traffic']['value']


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

