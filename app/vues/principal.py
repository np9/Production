from flask import render_template, jsonify, flash, redirect, url_for, request
from flask.ext.login import current_user
from app import app, db, modeles
import random
from app.outils import utile
from app.formulaires import reservation as rs
from app.outils import geographie
import json


# Redirection des pages web

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    if current_user.is_authenticated == False:
        form = rs.Demande_NonAuth()
    else:
        form = rs.Demande_Auth()

    if form.validate_on_submit():

        # Formattage de la date
        date_course = str(form.date_debut.data) + " " + \
            str(form.heures.data) + ":" + str(form.minutes.data) + ":00"

        # On insère l'utilisateur s'il n'est pas dans la base
        if current_user.is_authenticated == False:
            utilisateur = modeles.Utilisateur(
                telephone = form.telephone.data,
                prenom = form.prenom.data,
                nom = form.nom.data,
                email = form.mail.data,
                categorie = form.categorie.data,
                civilite = form.civilite.data
            )
            db.session.add(utilisateur)
            db.session.commit()

        # On construit les adresses pour les géolocaliser
        localisation_dep = ' '.join([
            form.numero_dep.data,
            form.adresse_dep.data,
            form.ville_dep.data
        ])

        localisation_arr = ' '.join([
            form.numero_arr.data,
            form.adresse_arr.data,
            form.ville_arr.data
        ])

        # Géocalisation des adressses de départ et d'arrivée
        positions = {
            'depart': geographie.geocoder(localisation_dep),
            'arrivee': geographie.geocoder(localisation_arr)
        }

        # Adresse de départ
        adresse_dep = modeles.Adresse(
            nom_rue = form.adresse_dep.data,
            numero = form.numero_dep.data,
            cp = form.cp_dep.data,
            ville = form.ville_dep.data,
            position = 'POINT({0} {1})'.format(
                positions['depart']['lat'],
                positions['depart']['lon']
            )
        )
        db.session.add(adresse_dep)
        db.session.commit()

        # Adresse d'arrivée
        adresse_arr = modeles.Adresse(
            nom_rue = form.adresse_arr.data,
            numero = form.numero_arr.data,
            cp = form.cp_arr.data,
            ville = form.ville_arr.data,
            position = 'POINT({0} {1})'.format(
                positions['arrivee']['lat'],
                positions['arrivee']['lon']
            )
        )
        db.session.add(adresse_arr)
        db.session.commit()

        # Création de la course
        nouvelle_course = modeles.Course(
            depart = adresse_dep.identifiant,
            arrivee = adresse_arr.identifiant,
            places = form.nb_passagers.data,
            commentaire = form.commentaire.data,
            debut = date_course,
            trouvee = False,
            finie = False
        )

        if current_user.is_authenticated:
            # Pas sur de ça
            current_user.categorie = form.categorie.data
            nouvelle_course.utilisateur = current_user.telephone
        else:
            nouvelle_course.utilisateur = form.telephone.data

        db.session.add(nouvelle_course)
        db.session.commit()

        # Création d'une nouvelle facture
        facture = modeles.Facture(
            course = nouvelle_course.numero,
            paiement = form.paiement.data,
            estimation = 0,
            montant = 0,
            rabais = 0
        )

        db.session.add(facture)
        db.session.commit()

        flash('La demande de réservation a été prise en compte.', 'positive')

        donnees = form.data
        return redirect(url_for('devis', form=donnees))
    return render_template('index.html', form=form, titre='Réserver un taxi')


@app.route('/devis')
def devis():
    form = request.args.get('form')
    form = form.replace("'", '"')
    donnees = json.loads(form)
    return render_template('devis.html', titre='Devis', donnees=donnees)


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
