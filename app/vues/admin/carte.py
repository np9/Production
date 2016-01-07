from flask import jsonify
from flask.ext.admin import BaseView, expose
from app import admin
from app import modeles
from app.vues.admin import VueModele

class VueCarte(BaseView):

    @expose('/')
    def index(self):
        return self.render('admin/carte.html')

    @expose('/rafraichir', methods=['POST'])
    def rafraichir(self):
        conducteurs = modeles.Conducteur.query.all()
        for conducteur in conducteurs:
            print(conducteur.geom)
        return jsonify({'donnees': conducteurs})

admin.add_view(
    VueCarte(
        name='Carte',
        url='carte'
    )
)
