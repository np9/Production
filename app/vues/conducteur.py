from flask import Blueprint, render_template
from app.outils.geographie import geocoder
from app import app, db, modeles
import psycopg2
import psycopg2.extras
import sys
# Créer un patron pour les vues conducteurs
conducteurbp = Blueprint('conducteurbp', __name__, url_prefix='/conducteur')


def gps(depart, arrivee):
    arrivee = geocoder(arrivee)
    base = 'https://maps.googleapis.com/maps/api/directions/json?'
    key = 'AIzaSyCBQSQ2Ze-8wEnZcT1V8__ug2WLdRmtdmA'
    url = '{0}'

@conducteurbp.route('/<numero>', methods=['GET', 'POST'])
def conducteur_accueil(numero):
    
    inp = db.session.execute("SELECT prenom, nom, ST_X(position) as lon, ST_Y(position) as lat, statut FROM conducteurs WHERE telephone = {0}".format(numero))
    inf = inp.fetchall()
    pnom = inf[0][0]
    nom = inf[0][1]
    lon = inf[0][2]
    lat = inf[0][3]
    libre = inf[0][4]
    return render_template('conducteur/accueil.html', titre='Conducteur', numero=numero, nom = nom, lon=lon, lat=lat, libre=libre)

@app.route('/conducteur/accueil', methods=['GET', 'POST'])
def statutActuel():
	lib = db.session.execute("SELECT libre FROM conducteurs where email='amiraayadi@wanadoo.fr'")
	rep = lib.fetchall()
	rep=str(rep)
	rep = rep[2]
	if rep=="T": 
		reponse= "Vous êtes actuellement libre"
	else: reponse="Vous êtes actuellement occupé"
	return render_template("conducteur/accueil.html",reponse = reponse)

@app.route('/occupe', methods=['GET', 'POST'])
def occupe():
	db.session.execute("UPDATE conducteurs SET libre = false where email='amiraayadi@wanadoo.fr'" )
	db.session.commit()
	lib1 = db.session.execute("SELECT libre FROM conducteurs where email='amiraayadi@wanadoo.fr'")
	rc = lib1.fetchall()
	return rc
	
@app.route('/libre', methods=['GET', 'POST'])
def libre():
	db.session.execute("UPDATE conducteurs SET libre = true where email='amiraayadi@wanadoo.fr'" )
	db.session.commit()
 
 
@app.route('/majlat', methods=['GET', 'POST'])
def majlat(lon, lat):
    db.session.execute("UPDATE conducteurs SET ST_X(position) ={0} and ST_X(position) ={1} true where email='amiraayadi@wanadoo.fr'".format(lat,lon) )
    db.session.commit()


'''
@app.route('/Attribution_Thomas') #Propositions de courses possibles
def Attribution_Thomas():
	lib = db.session.execute("SELECT numero, course, debut, fin FROM propositions P, courses C WHERE P.course = C.numero")
	rep = lib.fetchall()
	num = rep[0][1] #recuperation du numero de course de la première possible
	#recuperation seulement de l'heure de début et de fin
	a = rep[0][2]
	deb = a.isoformat()[11:19]
	b = rep[0][3]
	fin = b.isoformat()[11:19]
	return render_template("Attribution_Thomas.html", num = num, deb = deb, fin = fin)"
'''