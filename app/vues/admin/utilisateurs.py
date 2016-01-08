from app import admin
from app import modeles
from app import db
from app.vues.admin import VueModele


class VueUtilisateurContact(VueModele):

    ''' Informations de contact de l'utilisateur. '''

    can_create = True
    can_edit = True
    can_delete = True
    
    column_list = ['civilite','nom','prenom','telephone','email','adresse']    
    
    column_exclude_list = [
        '_mdp',
        'confirmation',
        'notification_email',
        'notification_sms',
        'inscription'
    ]

    column_searchable_list = [
        'prenom',
        'nom',
        'telephone'
    ]


admin.add_view(
    VueUtilisateurContact(
        modeles.Utilisateur,
        db.session,
        endpoint='utilisateur/contact',
        category='Utilisateur',
        name='Contact',
        menu_icon_type='glyph',
        menu_icon_value='glyphicon-earphone'
    )
)


class VueUtilisateurCompte(VueModele):

    ''' Informations sur le compte de l'utilisateur. '''

    can_create = True
    can_edit = True
    can_delete = True

    column_exclude_list = [
        '_mdp',
        'civilite',
        'email',
        'categorie',
        'fax'
    ]

    column_searchable_list = [
        'prenom',
        'nom', 
        'telephone'
    ]

    column_filters = [
        'notification_email',
        'notification_sms',
        'inscription'
    ]


admin.add_view(
    VueUtilisateurCompte(
        modeles.Utilisateur,
        db.session,
        endpoint='utilisateur/compte',
        category='Utilisateur',
        name='Compte',
        menu_icon_type='glyph',
        menu_icon_value='glyphicon-user'
    )
)
