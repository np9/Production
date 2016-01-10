from flask import render_template, jsonify, flash, redirect, url_for, request
from flask.ext.login import current_user
import json
from app import app, db, modeles
from app.outils import utile
from app.formulaires import reservation as rs
from app.outils import geographie
from app.devis import tarif


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():


    if current_user.is_authenticated == False:
        form = rs.Demande_NonAuth()
    else:
        form = rs.Demande_Auth()

    if form.validate_on_submit():
        flash('Le formulaire de réservation a été validé.', 'positive')

        demande = form.data

        if current_user.is_authenticated:
            demande['prenom'] = current_user.prenom
            demande['nom'] = current_user.nom
            demande['telephone'] = current_user.telephone
            demande['mail'] = current_user.email

        # Données de test
        demande['A-R'] = False
        demande['bagage'] = 0
        demande['gare'] = False
        demande['aeroport'] = False
        demande['animaux'] = 0

        print(demande)

        # Calculs de la tarification provisoire - création du devis
        devis = tarif.estimation(demande)
        print(devis)

        data = {'demande': demande,
                'devis': devis}

        return render_template('devis.html', data=data, titre='Devis')
    return render_template('index.html', form=form, titre='Réserver un taxi')


@app.route('/accepter', methods=['GET', 'POST'])
def accepter():

    # Récupération des données et formatage du JSON
    data = str(json.loads(request.data.decode()))
    data = data.replace('&#39;', '"')
    data = json.loads(data)
    demande = data['demande']

    # Formattage de la date
    date_course = str(demande['date_debut']) + " " + \
        str(demande['heures']) + ":" + str(demande['minutes']) + ":00"

    # On insère l'utilisateur s'il n'est pas dans la base
    if current_user.is_authenticated == False:
        utilisateur = modeles.Utilisateur(
            telephone=demande['telephone'],
            prenom=demande['prenom'],
            nom=demande['nom'],
            email=demande['mail'],
            civilite=demande['civilite'],
        )
        db.session.add(utilisateur)
        db.session.commit()

    # Géocalisation des adressses de départ et d'arrivée
    positions = {
        'depart': geographie.geocoder(demande['adresse_dep']),
        'arrivee': geographie.geocoder(demande['adresse_arr'])
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
        places=demande['nb_passagers'],
        commentaire=demande['commentaire'],
        debut=date_course,
        trouvee=False,
        finie=False
    )

    if current_user.is_authenticated:
        # Pas sur de ça
        nouvelle_course.utilisateur = current_user.telephone
    else:
        nouvelle_course.utilisateur = demande['telephone']

    db.session.add(nouvelle_course)
    db.session.commit()

    # Création d'une nouvelle facture
    facture = modeles.Facture(
        course=nouvelle_course.numero,
        paiement=demande['paiement'],
        estimation=0,
        montant=0,
        rabais=0
    )

    db.session.add(facture)
    db.session.commit()

    # Envoi d'un email
    if current_user.is_authenticated == False:
        adresse_mail = demande['mail']
    else:
        adresse_mail = current_user.email

    devis = data['devis']
    # Sujet du mail à envoyer
    sujet = 'Votre demande de réservation a été effectuée.'
    # Le corps du mail est un template écrit en HTML
    html = render_template('email/facture.html', devis=devis)
    # Envoyer le mail à l'utilisateur
    email.envoyer(adresse_mail, sujet, html)

    flash('La demande de réservation a été prise en compte.', 'positive')
    return jsonify({'statut': 'succes'})



@app.route('/carte')
def carte():
    return render_template('carte.html', titre='Carte')


@app.route('/carte_rafraichir', methods=['POST'])
def carte_rafraichir(self):
    conducteurs = modeles.Conducteur.query.all()
    geojson = [
        json.loads(
            db.session.scalar(
                ST_AsGeoJSON(
                    conducteur.position
                )
            )
        )
        for conducteur in conducteurs
    ]
    return jsonify({
        'positions': geojson,
        'conducteurs': conducteurs
    })


@app.route('/tarifs')
def tarifs():
    return render_template('tarifs.html', titre='Tarifs')


@app.route('/informations')
def informations():
    return render_template('informations.html', titre='Informations')


@app.route('/faq')
def faq():
    faq_data = utile.lire_json('app/static/data/faq.json')
    return render_template('faq.html', titre='FAQ', faq_data=faq_data)


@app.route('/contact')
def contact():
    return render_template('contact.html', titre='Contact')
