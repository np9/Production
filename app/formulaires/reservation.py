from flask.ext.wtf import Form
from wtforms import TextField, SelectField
from wtforms.validators import (Required, Length, Email, ValidationError,
                                EqualTo)


class Demande_NonAuth(Form):
    ''' Demande de réservation d'un taxi par un utilisateur non-connecté. '''

    nom = TextField(description='Nom')

    prenom = TextField(description='Prénom')

    telephone = TextField(validators=[
        Required(message='Veuillez renseigner votre numéro de téléphone.')
    ], description='Numéro de téléphone')

    mail = TextField(validators=[Email(
        message='Adresse email non valide')], description='Adresse email')

    civilite = SelectField('Civilité', choices=[
        ('monsieur', 'Monsieur'),
        ('madame', 'Madame')
    ])

    ville_dep = TextField(validators=[
        Required(message='Veuillez renseigner la ville de départ.'),
        Length(min=2)
    ], description="Ville de départ")

    cp_dep = TextField(validators=[
        Length(max=5)
    ], description='Code postal')

    adresse_dep = TextField(validators=[
        Required(message='Veuillez renseigner une adresse.'),
        Length(min=2)
    ], description='Adresse')

    numero_dep = TextField(validators=[
        Required(message='Veuillez renseigner un n° de rue.'),
        Length(min=1)
    ], description='Numéro')

    date_debut = TextField(validators=[
        Required(message='Veuillez renseigner une date de début')
    ], description='Date de début')

    ville_arr = TextField(validators=[
        Required(message="Veuillez renseigner la ville d'arrivée."),
        Length(min=2)
    ], description="Ville d'arrivée")

    cp_arr = TextField(validators=[
        Length(max=5)
    ], description='Code postal')

    adresse_arr = TextField(validators=[
        Required(message='Veuillez renseigner une adresse.'),
        Length(min=2)
    ], description='Adresse')

    numero_arr = TextField(validators=[
        Required(message='Veuillez renseigner un n° de rue.'),
        Length(min=1)
    ], description='Numéro')

    nb_passagers = SelectField('Nombre de passagers', choices=[
        (str(i), str(i))
        for i in range(1, 9)
    ])

    paiement = SelectField('Paiement', choices=[
        ('especes', 'Espèces'),
        ('carte', 'Carte Bleu'),
        ('cheque', 'Chèque'),
        ('am_express', 'American Express')
    ])

    categorie = SelectField('Catégorie', choices=[
        ('particulier', 'Particulier'),
        ('professionnel', 'Professionnel')
    ])

    commentaire = TextField(description="Commentaire")

    heures = SelectField('Heures', choices=[
        (str(i), str(i))
        for i in range(24)
    ])

    minutes = SelectField('Minutes', choices=[
        (str(i), str(i))
        for i in range(0, 60, 5)
    ])


class Demande_Auth(Form):

    ''' Demande de réservation d'un taxi par un utilisateur connecté. '''

    ville_dep = TextField(validators=[
        Required(message='Veuillez renseigner la ville de départ.'),
        Length(min=2)
    ], description="Ville de départ")

    cp_dep = TextField(validators=[
        Length(max=5)
    ], description='Code postal')

    adresse_dep = TextField(validators=[
        Required(message='Veuillez renseigner une adresse.'),
        Length(min=2)
    ], description='Adresse')

    numero_dep = TextField(validators=[
        Required(message='Veuillez renseigner un n° de rue.'),
        Length(min=1)
    ], description='Numéro')

    date_debut = TextField(validators=[
        Required(message='Veuillez renseigner une date de début')
    ], description='Date de début')

    ville_arr = TextField(validators=[
        Required(message="Veuillez renseigner la ville d'arrivée."),
        Length(min=2)
    ], description="Ville d'arrivée")

    cp_arr = TextField(validators=[
        Length(max=5)
    ], description='Code postal')

    adresse_arr = TextField(validators=[
        Required(message='Veuillez renseigner une adresse.'),
        Length(min=2)
    ], description='Adresse')

    numero_arr = TextField(validators=[
        Required(message='Veuillez renseigner un n° de rue.'),
        Length(min=1)
    ], description='Numéro')

    nb_passagers = SelectField('Nombre de passagers', choices=[
        (str(i), str(i))
        for i in range(1, 9)
    ])

    paiement = SelectField('Paiement', choices=[
        ('especes', 'Espèces'),
        ('carte', 'Carte Bleu'),
        ('cheque', 'Chèque'),
        ('am_express', 'American Express')
    ])

    categorie = SelectField('Catégorie', choices=[
        ('particulier', 'Particulier'),
        ('professionnel', 'Professionnel')
    ])

    commentaire = TextField(description="Commentaire")

    heures = SelectField('Heures', choices=[
        (str(i), str(i))
        for i in range(24)
    ])

    minutes = SelectField('Minutes', choices=[
        (str(i), str(i))
        for i in range(0, 60, 5)
    ])
