
from flask import request, Response, jsonify
from werkzeug.exceptions import HTTPException
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.contrib.geoa import ModelView as VueGeo
from flask.ext.admin.contrib.fileadmin import FileAdmin
from flask_admin import BaseView, expose
import os.path as op
from app import app
from app import admin
from app import modeles
from app import db

# Aléatoire pour la carte
import random
# Poour données sur la carte
import json 

class VueModele(ModelView):
    '''
    Vue de base qui implémente une authentification
    HTTP. Toutes les autres vues héritent de cette vue.
    '''
    
    # Afficher clé primaire
    column_display_pk = True
    
    # Afficher clé étrangère
    #please_do_show_fk_value = True
    column_display_fk = True
    column_hide_backrefs = True

    def is_accessible(self):
        auth = request.authorization or request.environ.get(
            'REMOTE_USER')  # workaround for Apache
        if not auth or (auth.username, auth.password) != app.config['ADMIN_CREDENTIALS']:
            raise HTTPException('', Response('Il faut rentrer les identifiants administrateur.', 401,
                                             {'WWW-Authenticate': 'Basic realm="Identifiants requis"'}
                                             ))
        return True
 
 
# Classe de la sous catégorie de l'utilisateur pour les infos à propos de la personne
class VueUtilisateurContact(VueModele):

    # Rendre impossible la création, la modification et la suppression
    can_create = False
    can_edit = True
    can_delete = False
    
    
    # Colonnes invisible
    column_exclude_list = ['_mdp','civilite','confirmation','notification_email','notification_sms','inscription']



    # Colonnes pour chercher
    column_searchable_list = ['prenom', 'nom','telephone']

    # Colonnes pour filtrer
    column_filters = ['categorie']


# Classe de la sous catégorie de l'utilisateur pour les infos administratives liées à l'utilisateur
class VueUtilisateurCompte(VueModele):

    # Rendre impossible la création, la modification et la suppression
    can_create = False
    can_edit = True
    can_delete = False
    
    
    # Colonnes invisible
    column_exclude_list = ['_mdp','civilite','email','categorie','fax']



    # Colonnes pour chercher
    column_searchable_list = ['prenom', 'nom','telephone']

    # Colonnes pour filtrer
    column_filters = [ 'confirmation','notification_email','notification_sms','inscription']


# Classe de la sous catégorie du conducteur pour les infos à propos de la personne
class VueConducteurContact(VueGeo) :

    # Rendre possible la création, la modification et la suppression
    can_create = True
    can_edit = True
    can_delete = True
    
    #colonnes à afficher
    #adresse a voir avec la jointure
    colnum_list = ['civilite','nom','prenom','telephone','email','adresse','categorie']
    
    #Colonnes pour chercher
    column_searchable_list = ['nom','prenom','telephone']
    
    #colonne à rentrer pour ajout d'un conducteur
    form_columns = ['telephone','civilite','email','date_naissance','fax','prenom','nom','statut','station','station_entree','position','adresse','inscription']

    # Colonne de filtre
    column_filters = ['civilite']


# Classe de la sous catégorie du conducteur liée à sa situation    
class VueConducteurSituation(VueGeo) :

    # Rendre possible la création, la modification et la suppression
    can_create = True
    can_edit = True
    can_delete = True
    
    # Colonnes à afficher
    column_list =['civilite','nom','prenom','telephone','situation','station','station_entree','position']    
    
    #Colonnes pour chercher
    column_searchable_list = ['nom','prenom','telephone']
    
    #colonne à rentrer pour ajout d'un conducteur
    form_columns = ['telephone','civilite','email','date_naissance','fax','prenom','nom','statut','station','station_entree','position','adresse','inscription']

    # Colonne de filtre
    column_filters = ['statut','station','civilite']

class VueVehicule(VueModele) :
    
    # Rendre possible la création, la modification et la suppression
    can_create = True
    can_edit = True
    can_delete = True

    #Colonnes pour chercher
    column_searchable_list = ['marque','couleur']  
    
    # Valeurs à rentrer pour ajout d'un véhicule
    form_columns = ['immatriculation','conducteur','places','couleur','marque','animaux','modele','american_express','carte_bleue','cheque','anglais','espagnol','allemand','vip','attelage','vbreak','voiture_basse','blacklist','mineur']


class VueStation(VueModele) :
        
    # Rendre possible la création, la modification et la suppression
    can_create = True
    can_edit = True
    can_delete = True

    # Colonnes pour chercher
    column_searchable_list = ['nom']

    # Colonne pour ajout d'une station
    form_columns = ['nom','adresse','distance_entree','distance_sortie']
 


class VueAdresse(VueGeo) :

    # Rendre possible la création, la modification et la suppression
    can_create = True
    can_edit = True
    can_delete = True
        
    # Colonne pour ajout d'une adresse
    form_columns = ['identifiant','nom_rue','numero','cp','ville','position','secteur']
    

# Facture
class VueFacture(VueModele) :
        
    # Rendre possible la création, la modification et la suppression
    can_create = True
    can_edit = True
    can_delete = True

    # Colonne pour ajout d'une facture
    form_columns = ['course','forfait','estimation','montant','rabais','paiement']
 

# Course
class VueCourse(VueModele) :
        
    # Rendre possible la création, la modification et la suppression
    can_create = True
    can_edit = True
    can_delete = True

    # Colonne pour ajout d'un utilisateur
    form_columns = ['numero','trouvee','finie','utilisateur','conducteur','places','priorite','debut','fin','retour','commentaire','bagages','animaux','gare','aeroport','depart','arrivee']
 

# Récuperer la position des conducteurs
def requetePosConduct() : 
    req = db.session.execute(
        '''
        SELECT position FROM conducteur
        ''')
    ligneCond = req.fetchall()
    print(ligneCond)

# Changement de place de la carte
@app.route('/carteVille', methods = ['POST'])
def carte_refresh (): 
    req = db.session.execute('SELECT position FROM Conducteurs WHERE nom = Ayadi')
    position = req.fetchall()
    return jsonify({'position' : position})
    


# Utilisateurs
admin.add_view(VueUtilisateurContact(modeles.Utilisateur, db.session, endpoint='contact', category='Utilisateur', name='contact', menu_icon_type='glyph', menu_icon_value='glyphicon-earphone'))
admin.add_view(VueUtilisateurCompte(modeles.Utilisateur, db.session, endpoint='compte', category='Utilisateur', name='compte', menu_icon_type='glyph', menu_icon_value='glyphicon-file'))

# Conducteurs
admin.add_view(VueConducteurSituation(modeles.Conducteur, db.session, endpoint='Situation', name = 'Situation', category ='Conducteur',menu_icon_type='glyph', menu_icon_value ='glyphicon-plane')) #taxi
admin.add_view(VueConducteurContact(modeles.Conducteur, db.session, endpoint='contact2', category='Conducteur', name='Contact', menu_icon_type='glyph', menu_icon_value ='glyphicon-earphone'))

# Vehicules
admin.add_view(VueVehicule(modeles.Vehicule, db.session))

# Stations
admin.add_view(VueStation(modeles.Station, db.session))

# Facture
admin.add_view(VueFacture(modeles.Facture, db.session))

# Course
admin.add_view(VueCourse(modeles.Course, db.session))

# Adresses
admin.add_view(VueAdresse(modeles.Adresse, db.session))


''' /!\ On a mis des \ avant les \''' car le SELECT... ne c'était mis en commentaire à cause de ça (ça faisait tout buguer) /!\
####################################
# Vue Utilisateur Catégorie Contact#
####################################
class VueUtilisateurContact(ModelView):
    @expose('/contact')
    def utilisateurContact(self) :
        req = db.session.execute(\'''
		SELECT nom, prenom, telephone, email, adresse, categorie 
		FROM Utilisateurs;
        \''')
        UtilisateurContact = req.fetchall()
        return self.render('contact.html',utilisateurs=UtilisateurContact)
admin.add_view(VueUtilisateurContact(None,db.session))
class VueCarte(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html', position=position)
admin.add_view(VueCarte())
'''
