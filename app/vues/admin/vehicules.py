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


class VueVehiculeType(VueVehicule) :
    column_list = [
        'immatriculation',
        'conducteur',
        'marque',
        'modele',
        'places',
        'couleur',
        'attelage',
        'vbreak',
        'voiture_basse'
    ]

admin.add_view(
    VueVehiculeType(
        modeles.Vehicule,
        db.session,
        endpoint = 'VehiculeType',
        category = 'Vehicule',
        name = 'Types de Véhicule',
        menu_icon_type='glyph',
        menu_icon_value ='glyphicon-wrench'
    )
)


class VueVehiculeClient(VueVehicule) :
    column_list = [
        'immatriculation',
        'conducteur',
        'vip',
        'mineur',
        'animaux',
        'anglais',
        'espagnol',
        'allemand'
    ]

admin.add_view(
    VueVehiculeClient(
        modeles.Vehicule,
        db.session,
        endpoint = 'VehiculeClient',
        category = 'Vehicule',
        name = 'Client admis',
        menu_icon_type='glyph',
        menu_icon_value ='glyphicon-ok'
    )
)


class VueVehiculePaiement(VueVehicule) :
    column_list = [
    'immatriculation',
    'conducteur',
    'carte_bleue',
    'american_express',
    'cheque'
    ]

admin.add_view(
    VueVehiculePaiement(
        modeles.Vehicule,
        db.session,
        endpoint = 'VehiculePaiement',
        category = 'Vehicule',
        name = 'Mode de Paiement',
        menu_icon_type='glyph',
        menu_icon_value ='glyphicon-eur'
    )
)

