from flask import Blueprint, render_template
from app import db

# Créer un patron pour les vues conducteurs
conducteurbp = Blueprint('conducteurbp', __name__, url_prefix='/conducteur')


@conducteurbp.route('/gps', methods=['POST'])
def conducteur_gps():
	return 'to do'


@conducteurbp.route('/<telephone>', methods=['GET'])
def conducteur_accueil(telephone):
	''' Affiche la page d'accueil d'un conducteur. '''
	requete = db.session.execute("SELECT telephone, prenom, nom, ST_X(position) as lon, ST_Y(position) as lat, statut FROM conducteurs WHERE telephone = '{0}'".format(telephone))
	resultat = requete.first()
	conducteur = {
		'telephone': resultat[0],
		'prenom': resultat[1],
		'nom': resultat[2],
		'lat': resultat[3],
		'lon': resultat[4],
		'statut': resultat[5]
	}
	return render_template('conducteur/accueil.html', titre='Conducteur', conducteur=conducteur)
