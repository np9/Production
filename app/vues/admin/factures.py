from app import admin
from app import modeles
from app import db
from app.vues.admin import VueModele

class VueFacture(VueModele):

    ''' Informations sur les factures. '''

    can_create = True
    can_edit = True
    can_delete = True

    form_columns = [
    	'course',
    	'forfait',
    	'estimation',
    	'montant',
    	'rabais',
    	'paiement'
    ]

admin.add_view(
	VueFacture(
		modeles.Facture,
		db.session
	)
)