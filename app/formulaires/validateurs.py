from wtforms import ValidationError
from app.outils import geographie

class Unique(object):

    '''
    Validateur fait maison pour s'assurer qu'un
    attribut est unique. Par exemple on ne veut
    pas qu'un utilisateur puisse utiliser une
    adresse email qui a déjà été utilisé pour
    un autre compte. Cette classe suppose qu'on
    utilise SQLAlchemy.
    '''

    def __init__(self, model, field, message):
        self.model = model
        self.field = field
        self.message = message

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)

class AdresseValide(object):

    '''
    Validateur fait maison pour s'assurer qu'une
    adresse est valide. C'est à dire qu'on a
    réussi à la géocoder en lat/lon.
    '''

    def __init__(self, adresse):
        self.adresse = adresse
        self.message = "Cette adresse n'est pas reconnue."

    def __call__(self, form, field):
        position = geographie.geocoder(localisation)
        if position['statut'] == 'echec':
            raise ValidationError(self.message)