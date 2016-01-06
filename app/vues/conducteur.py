from flask import Blueprint, render_template
from app.outils.geographie import geocoder

# Créer un patron pour les vues conducteurs
conducteurbp = Blueprint('conducteurbp', __name__, url_prefix='/conducteur')


def gps(depart, arrivee):
	arrivee = geocoder(arrivee)
	base = 'https://maps.googleapis.com/maps/api/directions/json?'
	key = 'AIzaSyCBQSQ2Ze-8wEnZcT1V8__ug2WLdRmtdmA'
	url = '{0}'

@conducteurbp.route('/', methods=['GET', 'POST'])
def conducteur_accueil():
	p = 'Thibault'
	return render_template('conducteur/accueil.html', titre='Conducteur', prenom=p)