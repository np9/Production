from app import admin
from app import modeles
from app import db
from app.vues.admin import VueModele

categorie = 'Conducteur'


class VueConducteurContact(VueModele):

    ''' Informations de contact du conducteur. '''

    can_create = True
    can_edit = True
    can_delete = True

    column_list = [
        'civilite',
        'nom',
        'prenom',
        'telephone',
        'email',
        'adresse',
        'categorie'
    ]

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

    column_filters = [
        'civilite'
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


class VueConducteurSituation(VueModele):

    ''' Informations sur la situation des conducteurs. '''

    can_create = True
    can_edit = True
    can_delete = True

    column_list = [
        'civilite',
        'nom',
        'prenom',
        'telephone',
        'situation',
        'station',
        'station_entree',
        'position'
    ]

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

    column_filters = [
        'statut',
        'station',
        'civilite'
    ]

admin.add_view(
    VueConducteurSituation(
        modeles.Conducteur,
        db.session,
        endpoint='conducteur/situation',
        category ='Conducteur',
        name='Situation',
        menu_icon_type='glyph',
        menu_icon_value ='glyphicon-plane'
    )
)
