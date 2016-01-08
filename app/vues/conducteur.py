from flask import Blueprint, render_template, request, flash, jsonify
from app.outils.geographie import geocoder
from app import app, db, modeles
import psycopg2
import psycopg2.extras
import sys
import json
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
	lib = db.session.execute("SELECT statut FROM conducteurs where telephone = {0}".format(numero))
	rep = lib.fetchall()
	rep=str(rep)
	rep = rep[2]
	if rep=="L": 
		reponse= "Vous êtes actuellement libre"
	elif rep=="O":
		reponse= "Vous êtes actuellement occupé "
	elif rep=="E":
		reponse= "Vous êtes actuellement en pause"
	else: reponse="Vous êtes actuellement inactif"
	return render_template('conducteur/accueil.html',reponse = reponse)

@app.route('/occupe', methods=['GET', 'POST'])
def occupe():
	data = json.loads(request.data.decode())
	num = str(data['numero'])[5:16]
	print(num)
	db.session.execute("UPDATE conducteurs SET statut = 'Occupé' where telephone = '{0}' ".format(num))
	db.session.commit()	
	return jsonify({
         'statut': 'success'
     })
	
@app.route('/libre', methods=['GET', 'POST'])
def libre():
	data = json.loads(request.data.decode())
	num = str(data['numero'])[5:16]
	print(num)
	db.session.execute("UPDATE conducteurs SET statut = 'Libre' where telephone = '{0}' ".format(num))
	db.session.commit()	
	return jsonify({
         'statut': 'success'
     })
 		
@app.route('/inactif', methods=['GET', 'POST'])
def inactif():
	data = json.loads(request.data.decode())
	num = str(data['numero'])[5:16]
	db.session.execute("UPDATE conducteurs SET statut='Inactif' where telephone = '{0}' ".format(num))
	db.session.commit()
	return jsonify({
         'statut': 'success'
     })

@app.route('/pause', methods=['GET', 'POST'])
def pause():
	data = json.loads(request.data.decode())
	num = str(data['numero'])[5:16]
	db.session.execute("UPDATE conducteurs SET statut='En pause' where telephone = '{0}' ".format(num))
	db.session.commit()
	return jsonify({
         'statut': 'success'
     })
	
@app.route('/majlat', methods=['GET', 'POST'])
def majlat():
	data = json.loads(request.data.decode())
	num = str(data['numero'])[5:16]
	print(num)
	#flash('Le formulaire de réservation a été validé.', 'positive')
	db.session.execute("UPDATE conducteurs SET position = 'POINT({0} {1})' where telephone = '{2}' ".format(data['lat'],data['lon'],num))
	db.session.commit()
	return jsonify({
         'statut': 'success'
     })
     
@app.route('/test', methods=['GET', 'POST'])
def test():
	return jsonify({
         'statut': 'succes'
     })     


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