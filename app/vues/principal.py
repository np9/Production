from flask import render_template, jsonify, flash, redirect, url_for
from flask.ext.login import current_user
from app import app, db, modeles
import random
from app.outils import utile
from app.formulaires import reservation as rs
from app.outils import geographie


# Redirection des pages web

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = rs.Demande()
    # Formattage de la date
    date_course = str(form.date_debut.data) + " " + \
        str(form.heures.data) + ":" + str(form.minutes.data) + ":00"
    if form.validate_on_submit():

        if current_user.is_authenticated == False:
            utilisateur = modeles.Utilisateur(
                telephone=form.telephone.data,
                prenom=form.prenom.data,
                nom=form.nom.data,
                email=form.mail.data,
                categorie=form.categorie.data
            )
            # Ajout de l'utilisateur à la BD
            db.session.add(utilisateur)
            db.session.commit()

        # Géolocaliser les adresses
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
        depart = {'position': geographie.geocoder(localisation_dep)}
        arrivee = {'position': geographie.geocoder(localisation_arr)}

        # Adresse de départ
        adresse_dep = modeles.Adresse(
            adresse=form.adresse_dep.data,
            numero=form.numero_dep.data,
            cp=form.cp_dep.data,
            ville=form.ville_dep.data,
            position='POINT({0} {1})'.format(
                depart['position']['lat'], depart['position']['lon'])
        )

        # Adresse d'arrivée
        adresse_arr = modeles.Adresse(
            adresse=form.adresse_arr.data,
            numero=form.numero_arr.data,
            cp=form.cp_arr.data,
            ville=form.ville_arr.data,
            position='POINT({0} {1})'.format(
                arrivee['position']['lat'], arrivee['position']['lon'])
        )
        # Ajouter l'adresse à la BD
        db.session.add(adresse_dep)
        db.session.add(adresse_arr)

        # Modification de la tarification appliquée à l'utilisateur si il est
        # connecté
        if current_user.is_authenticated:
            current_user.categorie = form.categorie.data

            # Création d'une nouvelle course pour un utilisateur connecté
            nouvelle_course = modeles.Course(
                utilisateur=current_user.telephone,
                depart=adresse_dep.identifiant,
                arrivee=adresse_arr.identifiant,
                places=form.nb_passagers.data,
                commentaire=form.commentaire.data,
                debut=date_course,
                trouvee=False,
                finie=False)
        else:
            # Création d'une nouvelle course pour un utilisateur non-connecté
            nouvelle_course = modeles.Course(
                utilisateur=form.telephone.data,
                depart=adresse_dep.identifiant,
                arrivee=adresse_arr.identifiant,
                places=form.nb_passagers.data,
                commentaire=form.commentaire.data,
                debut=date_course,
                trouvee=False,
                finie=False)

        # Ajout de la course à la BD
        db.session.add(nouvelle_course)
        db.session.commit()

        # Création d'une nouvelle facture
        nouvelle_facture = modeles.Facture(
            course=nouvelle_course.numero,
            paiement=form.paiement.data,
            estimation=0,
            montant=0,
            rabais=0
        )

        # Ajout de la facture à la BD
        db.session.add(nouvelle_facture)

        # Sauvegarde des transations
        db.session.commit()

        flash('La demande de réservation a été prise en compte.', 'positive')
        return redirect(url_for('index'))
    return render_template('index.html', form=form, titre='Réserver un taxi')


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
