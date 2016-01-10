from flask import Blueprint, render_template
from app.vues.api import outils
from app import db


apiconducteurbp = Blueprint('apiconducteurbp', __name__, url_prefix='/api/conducteurs')


@apiconducteurbp.route('/<telephone>', methods=['GET'])
def conducteur(telephone):
    ''' Retourne les informations pour un certain conducteur. '''
    requete = db.session.execute("SELECT * FROM conducteurs WHERE telephone='{}'".format(telephone))
    return outils.transformer_json(requete)


@apiconducteurbp.route('/propositions/<telephone>', methods=['GET'])
def conducteur_propositions(telephone):
    ''' Retourne les propositions pour un certain conducteur. '''
    requete = db.session.execute("SELECT * FROM propositions P WHERE P.conducteur = '{}' AND p.ordre = 1".format(telephone))
    return outils.transformer_json(requete)


@apiconducteurbp.route('/maj_statut/telephone=<telephone>&statut=<statut>', methods=['POST'])
def conducteur_maj_statut(telephone, statut):
    ''' Met à jour le statut d'un conducteur dans la base de données. '''
    requete = "UPDATE conducteurs SET statut = '{0}' WHERE telephone = '{1}' ".format(statut, telephone)
    return outils.executer(requete)


@apiconducteurbp.route('/maj_position/telephone=<telephone>&lat=<lat>&lon=<lon>', methods=['POST'])
def conducteur_maj_position(telephone, lat, lon):
    ''' Met à jour la position d'un conducteur dans la base de données. '''
    requete = "UPDATE conducteurs SET position = 'POINT({0} {1})' WHERE telephone = '{2}' ".format(lat, lon, telephone)
    print(requete)
    return outils.executer(requete)
