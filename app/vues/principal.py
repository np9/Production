from flask import render_template, jsonify, flash, redirect, url_for, request
from flask.ext.login import current_user
from app import app, db, modeles
import random
from app.outils import utile
from app.formulaires import reservation as rs
from app.outils import geographie
import json
from app.devis import calculer


# Redirection des pages web

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    if current_user.is_authenticated == False:
        form = rs.Demande_NonAuth()
    else:
        form = rs.Demande_Auth()

    if form.validate_on_submit():
        flash('Le formulaire de réservation a été validé.', 'positive')

        donnees = form.data

        if current_user.is_authenticated:
            donnees['prenom'] = current_user.prenom
            donnees['nom'] = current_user.nom
            donnees['telephone'] = current_user.telephone
            donnees['mail'] = current_user.email

        # Données de test
        donnees['A-R'] = 'False'
        donnees['bagage'] = '0'
        donnees['gare'] = 'False'
        donnees['aeroport'] = 'False'
        donnees['animaux'] = '0'
        donnees['categorie'] = 'particulier'

        # Calculs de la tarification provisoire - création du devis
        devis = calculer.tarifs(donnees)
        print(donnees)
        print(devis)

        return render_template('devis.html', donnees=donnees, devis=devis, titre='Devis')
    return render_template('index.html', form=form, titre='Réserver un taxi')


@app.route('/accepter', methods=['GET', 'POST'])
def accepter():

    # Récupération des données et formatage du JSON
    donnees = str(json.loads(request.data.decode()))
    donnees = donnees.replace('&#39;', '"')
    donnees = json.loads(donnees)

    # Formattage de la date
    date_course = str(donnees['date_debut']) + " " + \
        str(donnees['heures']) + ":" + str(donnees['minutes']) + ":00"

    # On insère l'utilisateur s'il n'est pas dans la base
    if current_user.is_authenticated == False:
        utilisateur = modeles.Utilisateur(
            telephone=donnees['telephone'],
            prenom=donnees['prenom'],
            nom=donnees['nom'],
            email=donnees['mail'],
            civilite=donnees['civilite'],
        )
        db.session.add(utilisateur)
        db.session.commit()

    # Géocalisation des adressses de départ et d'arrivée
    positions = {
        'depart': geographie.geocoder(donnees['adresse_dep']),
        'arrivee': geographie.geocoder(donnees['adresse_arr'])
    }

    # Adresse de départ
    adresse_dep = modeles.Adresse(
        position='POINT({0} {1})'.format(
            positions['depart']['lat'],
            positions['depart']['lon']
        )
    )
    db.session.add(adresse_dep)
    db.session.commit()

    # Adresse d'arrivée
    adresse_arr = modeles.Adresse(
        position='POINT({0} {1})'.format(
            positions['arrivee']['lat'],
            positions['arrivee']['lon']
        )
    )
    db.session.add(adresse_arr)
    db.session.commit()

    # Création de la course
    nouvelle_course = modeles.Course(
        depart=adresse_dep.identifiant,
        arrivee=adresse_arr.identifiant,
        places=donnees['nb_passagers'],
        commentaire=donnees['commentaire'],
        debut=date_course,
        trouvee=False,
        finie=False
    )

    if current_user.is_authenticated:
        # Pas sur de ça
        nouvelle_course.utilisateur = current_user.telephone
    else:
        nouvelle_course.utilisateur = donnees['telephone']

    db.session.add(nouvelle_course)
    db.session.commit()

    # Création d'une nouvelle facture
    facture = modeles.Facture(
        course=nouvelle_course.numero,
        paiement=donnees['paiement'],
        estimation=0,
        montant=0,
        rabais=0
    )

    db.session.add(facture)
    db.session.commit()

    flash('La demande de réservation a été prise en compte.', 'positive')
    return jsonify({'statut': 'succes'})


@app.route('/carte')
def carte():
    return render_template('carte.html', titre='Carte')


@app.route('/rafraichir_carte', methods=['POST'])
def rafraichir_carte():
    lat = random.uniform(48.8434100, 48.8634100)
    lon = random.uniform(2.3388000, 2.3588000)
    return jsonify({'position': [lat, lon]})


@app.route('/tarifs')
def tarifs():
    return render_template('tarifs.html', titre='Tarifs')


@app.route('/informations')
def informations():
    return render_template('informations.html', titre='Informations')


@app.route('/FAQ')
def faq():
    faq_data = utile.lire_json('app/static/data/faq.json')
    return render_template('faq.html', titre='FAQ', faq_data=faq_data)


@app.route('/contact')
def contact():
    return render_template('contact.html', titre='Contact')


@app.route('/api')
def api():
    return render_template('api.html', titre='API')
