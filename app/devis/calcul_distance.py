from urllib.request import urlopen
import json
import unicodedata
from app.outils.utile import requette_http

#fonction permettant de formater la chaîne de caractère
def formatage_url(adresse):
  #On remplace plusieurs espaces par un seul, puis les espaces par des +
    adresse = ' '.join(adresse.split())
    adresse = adresse.replace(' ','+')
  #On remplace les caractères spéciaux (accents, ponctuation ...)
    texte = unicodedata.normalize('NFKD', adresse)
    octets = texte.encode('ascii', 'ignore')
    adresse = octets.decode('utf-8')
    list_sc = [";",":","!",",",".","-","?","'","[","]","(",")","{","}"]
    adresse = ''.join([i if i not in list_sc else '' for i in adresse ])
  #On met la première lettre de l'adresse en majuscule et le reste en minuscule    
    adresse = adresse.capitalize()
    return adresse

#fonction permettant de formater l'url et de calculer les distances
def distance(depart, arrivee):
    if len(depart)<3 or len(arrivee)<3:
        return None
    else:    
        base = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
        origine = 'origins=' + formatage_url(depart)
        destination = '&destinations=' + formatage_url(arrivee)
        fin = '&mode=driving&language=fr-FR&key=AIzaSyCQnaoaMu6GVo3AwRzN62l0onao2TPN_u0'
        url = base + origine + destination + fin
        reponse = requette_http(url)
        return json.loads(reponse)       

#Fonction permettant de récupérer la distance
def recup_distance(json):
    resultat = json['rows'][0]['elements'][0]['distance']['value']
    resultat = round(resultat / 1000)
    return resultat
       
#Fonction permettant de récuperer l'heure
def recup_heure(json):
    resultat = json['rows'][0]['elements'][0]['duration']['value']
    resultat = round(resultat / 60)
    return resultat

#Tests
#a = distance('Toulouse','Paris')
#print(recup_distance(a))
#print(recup_heure(a))
    