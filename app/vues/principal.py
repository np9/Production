from flask import render_template, jsonify, flash, redirect, url_for
from app import app, db, modeles
import random
from app.outils import utile
from app.formulaires import utilisateur as fu
from app.outils import geographie


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = fu.Demande()
    print(form.validate())
    if form.validate_on_submit():
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

        position_dep = geographie.geocoder(localisation_dep)
        position_arr = geographie.geocoder(localisation_arr)

        adresse_dep = modeles.Adresse(
            adresse=form.adresse_dep.data,
            numero=form.numero_dep.data,
            cp=form.cp_dep.data,
            ville=form.ville_dep.data,
            position='POINT({0} {1})'.format(
                position_dep['lat'], position_dep['lon'])
        )

        adresse_arr = modeles.Adresse(
            adresse=form.adresse_arr.data,
            numero=form.numero_arr.data,
            cp=form.cp_arr.data,
            ville=form.ville_arr.data,
            position='POINT({0} {1})'.format(
                position_arr['lat'], position_arr['lon'])
        )
        # Ajouter l'adresse à la BD
        db.session.add(adresse_dep)
        db.session.add(adresse_arr)

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
