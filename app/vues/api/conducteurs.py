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
    return outils.executer(requete)


@apiconducteurbp.route('/accepter/numero=<numero>&course=<course>', methods=['GET'])
def rep_oui(numero, course):
    ''' Le conducteur répond 'OUI' à la proposition de la course détaillée. '''
    try:
        # Affectation du conducteur à cette course dans la table courses
        db.session.execute("UPDATE courses SET conducteur = '{0}' WHERE numero = '{1}' ".format(numero, course))
        # Date et heure au moment de la réponse du conducteur dans la table propositions
        db.session.execute("UPDATE propositions SET reponse = CURRENT_TIMESTAMP WHERE conducteur = '{0}' AND course = '{1}'".format(numero, course))
        # Statut = 'Occupé' dans la table conducteurs pour ce conducteur
        db.session.execute("UPDATE conducteurs SET statut = 'Occupé' WHERE telephone = '{}'".format(numero))
        db.session.commit()
        return jsonify({'status': 'success'})
    except:
        return jsonify({'status': 'failure'})

   
@apiconducteurbp.route('/refuser1/numero=<numero>&course=<course>', methods=['GET'])
def rep_non_1(numero, course):
    '''
    Le conducteur répond 'NON' à une proposition de course.
    Le conducteur n'a pas le détail de cette course.
    '''
    try:
        # Date et heure actualisées pour l'attribut station_entree dans la table conducteurs
        db.session.execute("UPDATE conducteurs SET station_entree = CURRENT_TIMESTAMP WHERE telephone = '{0}'".format(numero))
        # Date et heure au moment de la réponse du conducteur dans la table propositions
        db.session.execute("UPDATE propositions SET reponse = CURRENT_TIMESTAMP WHERE conducteur = '{0}' AND course = '{1}'".format(numero, course))
        # Statut = 'Non' dans la table propositions pour ce conducteur et cette course
        db.session.execute("UPDATE propositions SET statut ='Non' WHERE conducteur = '{0}' AND course = '{1}'".format(numero, course))
        db.session.commit()
        return jsonify({'status': 'success'})
    except:
        return jsonify({'status': 'failure'})

     
@apiconducteurbp.route('/refuser2/numero=<numero>&course=<course>', methods=['GET'])
def rep_non_2(numero, course):
    ''' Le conducteur répond 'NON' à la proposition de la course détaillée. '''
    try:
        # Pénalité pour ce conducteur dans la table conducteurs
        db.session.execute("UPDATE conducteurs SET penalite = CURRENT_TIMESTAMP WHERE telephone = '{0}'".format(numero))
        # Date et heure au moment de la réponse du conducteur dans la table propositions
        db.session.execute("UPDATE propositions SET reponse = CURRENT_TIMESTAMP WHERE conducteur = '{0}' AND course = '{1}'".format(numero, course))
        # Statut = 'Non' dans la table propositions pour ce conducteur et cette course
        db.session.execute("UPDATE propositions SET statut ='Non' WHERE conducteur = '{0}' AND course = '{1}'".format(numero, course))
        db.session.commit()
        return jsonify({'status': 'success'})
    except:
        return jsonify({'status': 'failure'})