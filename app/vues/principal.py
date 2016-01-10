from flask import render_template, jsonify
import json
from app import app, db, modeles
from app.outils import utile


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
