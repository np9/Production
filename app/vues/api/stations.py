from flask import Blueprint
from app.vues.api import outils
from app import db


apistationbp = Blueprint('apistationbp', __name__, url_prefix='/api/stations')



#Stations :
#Fonction qui renvoie adresse (ex : "001"), population par station (count chauffeurs), et res (je sais pas ce que c'est)
#Triés par adresse (ordre croissant)
@apistationbp.route('/getall/', methods=['GET'])
def getall():
    ''' Retourne les informations pour un certain conducteur. '''
    requete = db.session.execute("select s.adresse, count(telephone) population from stations s, conducteurs c where c.station = s.nom group by s.nom")
    json = outils.transformer_json(requete)
    return json

#Info Population :
#Prends en paramètre une adresse de station
#Renvoie tous les taxi present sur l'adresse + temps qu'ils ont sont	
@apistationbp.route('/toto/', methods=['GET'])
def toto():
    ''' Retourne les informations pour un certain conducteur. '''   
    requete = db.session.execute("select c.telephone, round((extract('epoch' from (CURRENT_TIMESTAMP - c.station_entree)))/60) temps from stations s, conducteurs c where c.station = s.nom and s.nom='Capitole'")
    json = outils.transformer_json(requete)
    return json


