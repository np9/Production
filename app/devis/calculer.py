from datetime import datetime, timedelta
from app.outils import calendrier
from app.outils import utile
from app.outils.distance import Parcours


def date_depart(demande):
    '''
    Extraire la date de départ d'une demande de course
    et la rendre en format datetime.
    '''
    date = demande['date_debut'].split('-')
    annee = int(date[0])
    mois = int(date[1])
    jour = int(date[2][:2])
    heure = demande['heures']
    minutes = demande['minutes']
    # Retourner la date en format datetime
    return datetime(annee, mois, jour, heure, minutes)


def duree_trajet(depart, arrivee, debut):
    ''' Calculer la durée d'un trajet. '''
    # Initialiser un trajet
    parcours = Parcours(depart, arrivee, debut)
    # Calculer la durée du trajet
    parcours.calculer()
    # Obtenir l'estimation de la fin du trajet en datetime
    duree = timedelta(minutes=parcours.duree) / 60
    distance = parcours.distance / 1000
    return {
        'duree': duree,
        'distance': distance
    }


def seuil(date, heure):
    ''' Retourne un seuil en format datetime. '''
    seuil = datetime(
        year=date.year,
        month=date.month,
        day=date.day,
        hour=heure
    )
    return seuil


def simuler(depart, arrivee, debut):
    '''
    Trouver la duree d'une course
    et le temps passé pendant le jour ou la nuit
    d'une course.
    '''

    # Calculer la durée du trajet
    course = duree_trajet(depart, arrivee, debut)
    duree = course['duree']
    distance = course['distance']

    # Choisir une date de départ de référence pour établir une fourchette
    reference_debut = datetime(
        year=debut.year,
        month=debut.month,
        day=debut.day,
        hour=10
    ) + timedelta(days=7)
    
    # Calculer la durée du trajet de référence
    reference = duree_trajet(depart, arrivee, debut)
    reference_duree = reference['duree']
    reference_distance = reference['distance']

    fin = debut + duree
    # A utiliser...
    ecart = abs(duree - reference_duree).seconds

    # Obtenir les seuils de début et de fin
    seuil_jour_debut = seuil(debut, heure=8).timestamp()
    seuil_jour_fin = seuil(fin, heure=8).timestamp()
    seuil_nuit_debut = seuil(debut, heure=19).timestamp()
    seuil_nuit_fin = seuil(fin, heure=19).timestamp()

    # Convertir les datetime en timestamp pour les comparer aux seuils
    debut = debut.timestamp()
    fin = fin.timestamp()

    # On pourra obtenir le temps passé la nuit à partir de celui passé le jour
    duree_jour = 0

    # La course commence pendant la journée du jour de départ
    if seuil_jour_debut < debut < seuil_nuit_debut:
        # La course finit pendant la journée du jour de départ
        if fin < seuil_nuit_debut:
            duree_jour += fin - debut
        # La course finit pendant la nuit du jour de départ
        else:
            duree_jour += seuil_jour_debut - debut
    # La course finit durant la journée du lendemain du jour de départ
    if seuil_jour_debut < seuil_jour_fin < fin:
        duree_jour += fin - seuil_jour_fin

    # Calculer les ratios jour/nuit
    ratio_jour = duree_jour / duree.seconds
    ratio_nuit = 1 - ratio_jour

    return {
        'duree': duree,
        'distance': distance,
        'ratios': {
            'jour': ratio_jour,
            'nuit': ratio_nuit
        }
    }
