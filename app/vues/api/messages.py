from flask import Blueprint, render_template, jsonify
from app.vues.api import outils
from app import db


apimessagebp = Blueprint('apimessagebp', __name__, url_prefix='/api/messages')

@apimessagebp.route('/derniers_messages', methods=['GET','POST'])
def derniers_messages():
    ''' Retourne les messages des dernières 24h. '''
    requete = db.session.execute("SELECT * FROM messages WHERE moment > CURRENT_TIMESTAMP - interval '1 day'")
    return outils.transformer_json(requete)