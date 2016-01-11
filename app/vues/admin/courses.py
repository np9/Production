from app import admin
from app import modeles
from app import db
from app.vues.admin import VueModele

class VueCourse(VueModele):

    ''' Informations sur les courses. '''

    can_create = True
    can_edit = True
    can_delete = True

    form_columns = [
    	'utilisateur',
    	'places',
    	'priorite',
        'debut',
        'commentaire',
        'bagages',
        'animaux',
	    'animaux_grands',
        'gare',
        'aeroport',
        'depart',
        'arrivee'
    ]

admin.add_view(
	VueCourse(
		modeles.Course,
		db.session
	)
)
