from flask import render_template, flash, jsonify, request
from flask.ext.login import current_user
from app.devis import tarif
from app.formulaires import reservation as rs
from app.outils import geographie, email, utile
from app import modeles
from app import app, db
import datetime
import json


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
        demande['gare'] = True
        demande['aeroport'] = True

        demande['debut'] = datetime.datetime.strptime(demande['date_debut'], '%d-%m-%Y %H:%M')

        # Convertir les valeurs
        for key in demande.keys():
            try:
                demande[key] = eval(demande[key])
            except:
                pass

        print(demande)
        # Calcul de la tarification provisoire
        devis = tarif.estimation(demande)


        data = {
            'demande': demande,
            'devis': devis
        }


        return render_template('devis.html', data=data, titre='Devis')
    return render_template('index.html', form=form, titre='Réserver un taxi')


@app.route('/accepter', methods=['GET', 'POST'])
def accepter():

    # Récupération des données et formatage du JSON
    data = request.get_json()

    data = data.replace('&#39;', '"')

    data = eval(data)

    demande = data['demande']

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
        depart = adresse_dep.identifiant,
        arrivee = adresse_arr.identifiant,
        places = demande['nb_passagers'],
        commentaire = demande['commentaire'],
        debut = demande['debut'],
        trouvee = False,
        finie = False,
        animaux = demande['nb_animaux'],
        bagages = demande['nb_bagages'],
        animaux_grands = demande['animaux_grands']
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
        type_paiement=demande['paiement'],
        estimation_1=0,
        montant=0
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
    sujet = 'Votre demande de réservation a été prise en compte.'
    # Le corps du mail est un template écrit en HTML
    html = render_template('email/facture.html', devis=devis)
    # Envoyer le mail à l'utilisateur
    email.envoyer(adresse_mail, sujet, html)

    flash('La demande de réservation a été prise en compte.', 'positive')
    return jsonify({'statut': 'succes'})
