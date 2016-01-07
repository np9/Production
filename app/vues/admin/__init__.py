from flask import request, Response
from werkzeug.exceptions import HTTPException
from flask.ext.admin.contrib.sqla import ModelView
from app import app


class VueModele(ModelView):
    '''
    Vue de base qui implémente une authentification
    HTTP. Toutes les autres vues héritent de celle-ci.
    '''

    # Edition des données dans une fenête modale
    create_modal = True
    edit_modal = True

    # Afficher la clé primaire dans les vues
    column_display_pk = True

    # Configuration pour affichier les liens
    column_hide_backrefs = False
    column_display_all_relations = True

    def is_accessible(self):
        auth = request.authorization or request.environ.get(
            'REMOTE_USER')  # workaround for Apache
        if not auth or (auth.username, auth.password) != app.config['ADMIN_CREDENTIALS']:
            message = 'Il faut rentrer les identifiants administrateur.'
            raise HTTPException('', Response(message, 401, {
                'WWW-Authenticate': 'Basic realm="Identifiants requis"'
            }))
        return True
