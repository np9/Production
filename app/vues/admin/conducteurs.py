from app import admin
from app import modeles
from app import db
from app.vues.admin import VueModele

categorie = 'Conducteur'

# Ajout penalité
# + oui non penalite


class VueConducteur(VueModele) :

    can_create = True
    can_edit = True
    can_delete = True

    column_searchable_list = [
        'nom',
        'prenom',
        'telephone'
    ]

    form_columns = [
        'telephone',
        'civilite',
        'email',
        'date_naissance',
        'fax',
        'prenom',
        'nom',
        'statut',
        'station',
        'station_entree',
        'position',
        'adresse',
        'inscription'
    ]


class VueConducteurContact(VueConducteur):

    ''' Informations de contact du conducteur. '''
    
    
    column_list = [
        'civilite',
        'nom',
        'prenom',
        'telephone',
        'email',
        'adresse'
    ]


admin.add_view(
    VueConducteurContact(
        modeles.Conducteur,
        db.session,
        endpoint='conducteur/contact',
        category='Conducteur',
        name='Contact',
        menu_icon_type='glyph',
        menu_icon_value ='glyphicon-earphone'
    )
)


class VueConducteurSituation(VueConducteur):

    ''' Informations sur la situation des conducteurs. '''

    column_list = [
        'civilite',
        'nom',
        'prenom',
        'telephone',
        'statut',
        'station',
        'station_entree',
        'position'
    ]

    column_filters = [
        'statut',
        'station'
    ]

admin.add_view(
    VueConducteurSituation(
        modeles.Conducteur,
        db.session,
        endpoint='conducteur/situation',
        category ='Conducteur',
        name='Situation',
        menu_icon_type='glyph',
        menu_icon_value ='glyphicon-road'
    )
)


class VueConducteurPenalite(VueConducteur) :

    #colonnes à afficher
    colnum_list = ['civilite','nom','prenom','telephone','penalite']
      

admin.add_view(
    VueConducteurPenalite(
        modeles.Conducteur,
        db.session,
        endpoint='penalite',
        category='Conducteur',
        name='Penalite',
        menu_icon_type='glyph',
        menu_icon_value ='glyphicon-remove'
    )
)