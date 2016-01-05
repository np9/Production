from flask.ext.wtf import Form
from wtforms import TextField, SelectField
from wtforms.validators import (Required, Length, Email, ValidationError,
                                EqualTo)


class Demande(Form):

    ''' Demande de réservation d'un taxi par un utilisateur. '''

    ville_dep = TextField(validators=[Required(message='Veuillez renseigner la ville de départ.'), Length(
        min=2)], description="Ville de départ")
    cp_dep = TextField(description='Code postal', validators=[Length(max=5)])
    adresse_dep = TextField(
        validators=[Required(message='Veuillez renseigner une adresse.'), Length(min=2)], description='Adresse')
    numero_dep = TextField(
        validators=[Required(message='Veuillez renseigner un n° de rue.'), Length(min=1)], description='Numéro')

    date_debut = TextField(
        validators=[Required(message='Veuillez renseigner une date de début')], description='Date de début')

    ville_arr = TextField(validators=[Required(message="Veuillez renseigner la ville d'arrivée."), Length(
        min=2)], description="Ville d'arrivée")
    cp_arr = TextField(description='Code postal', validators=[Length(max=5)])
    adresse_arr = TextField(
        validators=[Required(message='Veuillez renseigner une adresse.'), Length(min=2)], description='Adresse')
    numero_arr = TextField(
        validators=[Required(message='Veuillez renseigner un n° de rue.'), Length(min=1)], description='Numéro')

    nb_passagers = SelectField('Nombre de passagers', choices=[
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4')
    ])

    paiement = SelectField('Programming Language', choices=[
        ('especes', 'Espèces'), ('carte', 'Carte Bleu'), ('cheque', 'Chèque'), ('am_express', 'American Express')])

    categorie = SelectField('Catégorie', choices=[
        ('particulier', 'Particulier'), ('professionnel', 'Professionnel')])

    commentaire = TextField(description="Commentaire")

    heures = SelectField('Heures', choices=[
        ('00', '00'), ('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'), ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'), ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23')])

    minutes = SelectField('Minutes', choices=[
        ('00', '00'), ('05', '05'), ('10', '10'), ('15', '15'), ('20', '20'), ('25', '25'), ('30', '30'), ('35', '35'), ('40', '40'), ('45', '45'), ('50', '50'), ('55', '55')])
