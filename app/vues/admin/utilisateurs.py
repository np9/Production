from app import admin
from app import modeles
from app import db
from app.vues.admin import VueModele

class VueUtilisateur(VueModele) :

    can_create = True
    can_edit = True
    can_delete = True
    
    column_searchable_list = [
        'prenom',
        'nom',
        'telephone'
    ]


    column_exclude_list = [
        '_mdp'
    ]

    form_columns = [
        'civilite',
        'nom',
        'prenom',
        'telephone',
        'email',
        'fax',
        'notification_email',
        'notification_sms',
        'confirmation',
        'inscription',
        'adresse'
        #'_mdp'
    ]


class VueUtilisateurContact(VueUtilisateur):

    ''' Informations de contact de l'utilisateur. '''

    column_list = [
        'civilite',
        'nom',
        'prenom',
        'telephone',
        'fax',
        'email',
        'adresse'
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


class VueUtilisateurCompte(VueUtilisateur):

    ''' Informations sur le compte de l'utilisateur. '''

    column_list = [
        'nom',
        'prenom',
        'telephone',
        'confirmation',
        'notification_email',
        'notification_sms',
        'inscription'
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
