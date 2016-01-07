from flask import Blueprint, jsonify
from app import app, db
from app.formulaires import utilisateur as fu
import pandas as pd
import datetime
import time

apibp = Blueprint('apibp', __name__, url_prefix='/api')


def nettoyer(colonne):
    # Convertir les dates au format iso
    if colonne.dtype == 'datetime64[ns]':
        colonne = colonne.apply(lambda x: x.isoformat())
    # Convertir les booléens et NoneType en string
    if colonne.dtype == 'bool':
        colonne = colonne.apply(lambda x: 'True' if x is True else 'False')
    colonne = colonne.apply(lambda x: 'None' if x is None else x)
    return colonne


def to_json(numero):
    requete = db.session.execute("SELECT * FROM conducteurs WHERE telephone = {}".format(numero))
    attributs = requete.keys()
    lignes = requete.fetchall()
    table = pd.DataFrame(lignes, columns=attributs)
    table = table.apply(nettoyer)
    json = table.to_dict(orient='records')
    return json


@apibp.route('/conducteurs/<numero>', methods=['GET'])
def api_table(numero):
    try:
        json = to_json(numero)
        return jsonify({'data': json, 'status': 'success'})
    except:
        return jsonify({'status': 'failure'})
   
@apibp.route('/conducteurs/maj_position/numero=<numero>&lat=<lat>&long=<long>', methods=['GET'])
def maj_position(numero, lat, long):
    try:
        db.session.execute("UPDATE conducteurs SET position = 'POINT({0} {1})' where telephone = '{2}' ".format(lat, long, numero))
        db.session.commit()        
        return jsonify({'status': 'success'})
    except:
        return jsonify({'status': 'failure'})
        
@apibp.route('/conducteurs/maj_statut/numero=<numero>&statut=<statut>', methods=['GET'])
def maj_statut(numero, statut):
    try:
        db.session.execute("UPDATE conducteurs SET statut = '{0}' where telephone = '{1}' ".format(statut, numero) )
        db.session.commit()
        return jsonify({'status': 'success'})
    except:
        return jsonify({'status': 'failure'})
        
def demande_course(numero):
    requete = db.session.execute("SELECT * FROM propositions p, courses c WHERE p.course = c.numero AND p.ordre = 1 AND p.conducteur = {}".format(numero))
    attributs = requete.keys()
    lignes = requete.fetchall()
    table = pd.DataFrame(lignes, columns=attributs)
    table = table.apply(nettoyer)
    json = table.to_dict(orient='records')
    return json


@apibp.route('/conducteurs/demande_course/<numero>', methods=['GET'])
def api_demande_course(numero):
    try:
        json = demande_course(numero)
        return jsonify({'data': json, 'status': 'success'})
    except:
        return jsonify({'status': 'failure'})
