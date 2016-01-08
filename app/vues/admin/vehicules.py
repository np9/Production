from app import admin
from app import modeles
from app import db
from app.vues.admin import VueModele

class VueVehicule(VueModele):

    ''' Informations sur les véhicules. '''

    can_create = True
    can_edit = True
    can_delete = True

    column_searchable_list = [
    	'marque',
    	'couleur'
    ]

    form_columns = [
    	'immatriculation',
    	'conducteur',
    	'places',
    	'couleur',
    	'marque',
    	'animaux',
    	'modele',
    	'american_express',
        'carte_bleue',
        'cheque',
        'anglais',
        'espagnol',
        'allemand',
        'vip',
        'attelage', 
       	'vbreak',
       	'voiture_basse',
       	'mineur'
    ]

admin.add_view(
	VueVehicule(
		modeles.Vehicule,
		db.session
	)
)
