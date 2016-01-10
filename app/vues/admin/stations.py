from app import admin
from app import modeles
from app import db
from app.vues.admin import VueModele

class VueStation(VueModele):

    ''' Informations sur les stations. '''

    can_create = True
    can_edit = True
    can_delete = True

    column_list = [
        'nom',
        'adresse',
        'distance_entree',
        'distance_sortie'
    ]

    column_searchable_list = [
    	'nom'
    ]

    form_columns = [
    	'nom',
    	'adresse',
    	'distance_entree',
    	'distance_sortie'
    ]

admin.add_view(
	VueStation(
		modeles.Station,
		db.session
	)
)