from app import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from flask.ext.login import UserMixin
from geoalchemy2 import Geometry


class Utilisateur(db.Model, UserMixin):

    ''' Un utilisateur du site web. '''

    __tablename__ = 'utilisateurs'

    telephone = db.Column(db.String, primary_key=True)
    civilite = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    confirmation = db.Column(db.Boolean)
    prenom = db.Column(db.String)
    nom = db.Column(db.String)
    fax = db.Column(db.String)
    notification_email = db.Column(db.Boolean)
    notification_sms = db.Column(db.Boolean)
    inscription = db.Column(db.DateTime)
    adresse = db.Column(db.Integer, db.ForeignKey('adresses.identifiant'))
    _mdp = db.Column(db.String)

    @hybrid_property
    def mdp(self):
        return self._mdp

    @mdp.setter
    def _set_password(self, plaintext):
        self._mdp = bcrypt.generate_password_hash(plaintext)

    def check_password(self, plaintext):
        # A changer, problème d'UTF-8 avec PostgreSQL
        return True
        return bcrypt.check_password_hash(self.mdp, plaintext)

    def get_id(self):
        return self.telephone


class Notification(db.Model):

    ''' Une notification envoyée à un utilisateur. '''

    __tablename__ = 'notifications'

    utilisateur = db.Column(db.String, db.ForeignKey('utilisateurs.telephone'))
    course = db.Column(db.Integer, db.ForeignKey('courses.numero'))
    moment = db.Column(db.DateTime)
    sujet = db.Column(db.String)

    __table_args__ = (
        db.PrimaryKeyConstraint('utilisateur', 'course', 'moment',
                                name='pk_notifications'),
    )


class Bannissement(db.Model):

    ''' Un bannissement d'un utilisateur. '''

    __tablename__ = 'bannissements'

    utilisateur = db.Column(db.String, db.ForeignKey('utilisateurs.telephone'))
    debut = db.Column(db.DateTime)
    fin = db.Column(db.DateTime)
    raison = db.Column(db.String)

    __table_args__ = (
        db.PrimaryKeyConstraint('utilisateur', 'debut', name='pk_bannissements'),
    )


class Conducteur(db.Model):

    ''' Un conducteur de taxi. '''

    __tablename__ = 'conducteurs'

    telephone = db.Column(db.String, primary_key=True)
    numero_imei = db.Column(db.String)
    civilite = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    date_naissance = db.Column(db.Date)
    fax = db.Column(db.Integer)
    prenom = db.Column(db.String)
    nom = db.Column(db.String)
    statut = db.Column(db.String)
    station = db.Column(db.String, db.ForeignKey('stations.nom'))
    station_entree = db.Column(db.DateTime)
    position = db.Column(Geometry('POINT'))
    adresse = db.Column(db.Integer, db.ForeignKey('adresses.identifiant'))
    inscription = db.Column(db.DateTime)
    debut_penalite = db.Column(db.DateTime)


class Message(db.Model):

    ''' Un message envoyé à un conducteur. '''

    __tablename__ = 'messages'

    conducteur = db.Column(db.String, db.ForeignKey('conducteurs.telephone'))
    moment = db.Column(db.DateTime)
    sujet = db.Column(db.String)

    __table_args__ = (
        db.PrimaryKeyConstraint('conducteur', 'moment', name='pk_messages'),
    )


class Position(db.Model):

    ''' Une position d'un conducteur à un moment donné. '''

    __tablename__ = 'positions'

    conducteur = db.Column(db.String, db.ForeignKey('conducteurs.telephone'))
    moment = db.Column(db.DateTime)
    position = db.Column(Geometry('POINT'))
    statut = db.Column(db.String)

    __table_args__ = (
        db.PrimaryKeyConstraint('conducteur', 'moment', name='pk_positions'),
    )


class Vehicule(db.Model):

    ''' Une vehicule appartient à un conducteur. '''

    __tablename__ = 'vehicules'

    immatriculation = db.Column(db.String, primary_key=True)
    conducteur = db.Column(db.String, db.ForeignKey('conducteurs.telephone'))
    places = db.Column(db.Integer, db.CheckConstraint('1 <= places And places <= 10'))
    couleur = db.Column(db.String)
    marque = db.Column(db.String)
    animaux = db.Column(db.Boolean)
    modele = db.Column(db.String)
    american_express = db.Column(db.Boolean)
    carte_bleue = db.Column(db.Boolean)
    cheque = db.Column(db.Boolean)
    anglais = db.Column(db.Boolean)
    espagnol = db.Column(db.Boolean)
    allemand = db.Column(db.Boolean)
    vip = db.Column(db.Boolean)
    attelage = db.Column(db.Boolean)
    vbreak = db.Column(db.Boolean)
    voiture_basse = db.Column(db.Boolean)
    mineur = db.Column(db.Boolean)


class Adresse(db.Model):

    ''' Un adresse géographique. '''

    __tablename__ = 'adresses'

    identifiant = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nom_rue = db.Column(db.String)
    numero = db.Column(db.String)
    cp = db.Column(db.Integer)
    ville = db.Column(db.String)
    adr_complete = db.Column(db.String)
    position = db.Column(Geometry('POINT'))
    station = db.Column(db.String, db.ForeignKey('stations.nom'))


class Station(db.Model):

    ''' Une station contenant des taxis. '''

    __tablename__ = 'stations'

    nom = db.Column(db.String, primary_key=True)
    adresse = db.Column(db.Integer, db.ForeignKey('adresses.identifiant'))
    distance_entree = db.Column(db.Float, db.CheckConstraint('0 <= distance_entree'))
    distance_sortie = db.Column(db.Float, db.CheckConstraint('0 <= distance_sortie'))

    __table_args__ = (
        db.CheckConstraint('distance_entree < distance_sortie',
                           name='entree_inf_sortie_check'),
    )


class Course(db.Model):

    ''' Une demande de course qui devient une course terminée. '''

    __tablename__ = 'courses'

    numero = db.Column(db.Integer, autoincrement=True, primary_key=True)
    trouvee = db.Column(db.Boolean)
    finie = db.Column(db.Boolean)
    utilisateur = db.Column(db.String, db.ForeignKey('utilisateurs.telephone'))
    conducteur = db.Column(db.String, db.ForeignKey('conducteurs.telephone'))
    places = db.Column(db.Integer, db.CheckConstraint('1 <= places'))
    priorite = db.Column(db.String)
    debut = db.Column(db.DateTime)
    fin = db.Column(db.DateTime)
    commentaire = db.Column(db.String)
    depart = db.Column(db.Integer, db.ForeignKey('adresses.identifiant'))
    arrivee = db.Column(db.Integer, db.ForeignKey('adresses.identifiant'))
    bagages = db.Column(db.Integer)
    animaux = db.Column(db.Integer)
    animaux_grands = db.Column(db.Boolean)
    gare = db.Column(db.Boolean)
    aeroport = db.Column(db.Boolean)
    entreprise = db.Column(db.String, db.ForeignKey('entreprises.nom'))
    distance_estimee = db.Column(db.Float)


    __table_args__ = (
        db.CheckConstraint('debut < fin', name='debut_inf_fin_check'),
    )


class Etape(db.Model):

    ''' Une étape d'une course. '''

    __tablename__ = 'etapes'

    course = db.Column(db.Integer, db.ForeignKey('courses.numero'))
    moment = db.Column(db.DateTime)
    position = db.Column(Geometry('POINT'))

    __table_args__ = (
        db.PrimaryKeyConstraint('course', 'moment', name='pk_etapes'),
    )


class Proposition(db.Model):

    ''' Une proposition de course faite à un conducteur. '''

    __tablename__ = 'propositions'

    iteration = db.Column(db.Integer)
    course = db.Column(db.Integer, db.ForeignKey('courses.numero'))
    conducteur = db.Column(db.String, db.ForeignKey('conducteurs.telephone'))
    proposition = db.Column(db.DateTime)
    reponse = db.Column(db.DateTime)
    statut = db.Column(db.String)
    raison = db.Column(db.String)
    ordre = db.Column(db.Integer)
    meme_station = db.Column(db.Boolean)

    __table_args__ = (
        db.PrimaryKeyConstraint('iteration', 'course', 'conducteur', name='pk_proposition'),
    )


class Facture(db.Model):

    ''' Une facture relative à une course. '''

    __tablename__ = 'factures'

    course = db.Column(db.Integer, db.ForeignKey('courses.numero'),
                       primary_key=True)
    montant = db.Column(db.Float, db.CheckConstraint('0 <= montant'))
    type_paiement = db.Column(db.String)
    estimation_1 = db.Column(db.Float)
    estimation_2 = db.Column(db.Float)


class Forfait(db.Model):

    __tablename__ = 'forfaits'

    entreprise = db.Column(db.String, db.ForeignKey('entreprises.nom'))
    destination_1 = db.Column(db.Integer, db.ForeignKey('adresses.identifiant'))
    destination_2 = db.Column(db.Integer, db.ForeignKey('adresses.identifiant'))
    tarif = db.Column(db.String)
    montant = db.Column(db.Float)
    
    __table_args__ = (
        db.PrimaryKeyConstraint('entreprise', 'destination_1', 'destination_2',
                                'tarif', name='pk_forfait'),
    )


class Entreprise(db.Model):

    __tablename__ = 'entreprises'

    nom = db.Column(db.String, primary_key=True)
    email = db.Column(db.String)
    telephone = db.Column(db.String)
    majoration = db.Column(db.Float)
    montant_en_cours = db.Column(db.Float)
    adresse = db.Column(db.Integer, db.ForeignKey('adresses.identifiant'))


class Paiement(db.Model):

    __tablename__ = 'paiements'

    entreprise = db.Column(db.String, db.ForeignKey('entreprises.nom'))
    mois = db.Column(db.String)
    annee = db.Column(db.Integer)
    montant = db.Column(db.Float)

    __table_args__ = (
        db.PrimaryKeyConstraint('entreprise', 'mois', 'annee', name='pk_paiement'),
    )
