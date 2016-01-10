from datetime import datetime, timedelta
from app.outils import geographie as geo
from app.outils import utile
from app.outils import calendrier
from app.devis import calculer


def calculer_supplement(demande, supplements):
    ''' Calcul des suppléments. '''
    supplement = 0
    # Bagages
    supplement += int(demande['bagages']) * supplements['bagage']
    # Animaux
    supplement += int(demande['animaux']) * supplements['animal']
    # Passagers supplémentaires
    supplement += max(0, demande['nb_passagers'] - 4) * supplements['personne_sup']
    # Trajet à vide (ça ne m'a pas l'air bon, à discuter)
    supplement += supplements['trajet_a_vide']
    # Prise en charge à la gare
    if demande['gare'] is True:
        supplement += supplements['gare']
    # Prise en charge à l'aéroport
    if demande['aeroport'] is True:
        supplement += supplements['aeroport']
    # Tarif supplémentaire appliqué à un trajet ralenti (pas sur de ce que vous essayez de faire)
    #estimation = float(tarif.type_tarif(demande)[4]) * float(PtR['Prix'])/3600
    return supplement


def estimation(demande):
    ''' Calculer le devis d'une demande. '''

    # On récupère les tarifs applicables
    tarifs = utile.lire_json('app/devis/data/tarifs.json')
    supplements = utile.lire_json('app/devis/data/supplements.json')

    # Prise en charge de départ
    prise_en_charge = supplements['prise_en_charge']

    # Extraction des information de départ
    depart = geo.geocoder(demande['adresse_dep'])
    arrivee = geo.geocoder(demande['adresse_arr'])
    debut = calculer.date_depart(demande)

    # Simulation de la course
    simulation = calculer.simuler(depart, arrivee, debut)
    duree = simulation['duree']
    distance = simulation['distance']
    jour = simulation['ratios']['jour']
    nuit = simulation['ratios']['nuit']

    # Savoir si c'est un jour ferié ou un dimanche
    date = '{0}/{1}'.format(debut.day, debut.month)
    jours_feries = calendrier.feries(debut.year)
    ferie = date in jours_feries
    dimanche = debut.weekday() == 6

    # Décider du tarif à appliquer
    if ferie or dimanche:
        prix_par_km = tarifs['D']
    else:
        prix_par_km = jour * tarifs['C'] + nuit * tarifs['D']

    # Calculer le prix de la course
    montant = distance * prix_par_km

    # Calculer le supplément
    supplement = calculer_supplement(demande, supplements)

    # Calcul du total
    total = montant + supplement
    # Prise en compte du tarif minimum
    total = max(total, supplements['tarif_minimum'])

    # On retourne l'estimation à travers un dictionnaire de données
    # Je pense qu'il y'a des choses qui ont été oubliées, par exemple
    # le passage à vide et la tarif pour un trajet ralenti, faites
    # attention
    estimation = {
        'prix': {
            'montant': round(montant, 2),
            'supplement': round(supplement, 2),
            'total': round(total, 2)
        },
        'detail': {
            'parcours': {
                'duree': duree,
                'distance': distance,
                'prix_par_km': prix_par_km
            },
            'bagages': {
                'nb': demande['bagages'],
                'prix': supplements['bagage'],
                'total': demande['bagages'] * supplements['bagage']
            },
            'animaux': {
                'nb': demande['animaux'],
                'prix': supplements['animal'],
                'total': demande['animaux'] * supplements['animal']
            },
            'personnes': {
                'nb': demande['nb_passagers'],
                'supplementaires': {
                    'nb': max(0, demande['nb_passagers'] - 4),
                    'prix': supplements['personne_sup'],
                    'total': max(0, demande['nb_passagers'] - 4) * supplements['personne_sup']
                }
            },
            'gare': {
                'prise_en_charge': demande['gare'],
                'prix': 0 if not demande['gare'] else supplements['gare']
            },
            'aeroport': {
                'prise_en_charge': demande['aeroport'],
                'prix': 0 if not demande['aeroport'] else supplements['aeroport']
            },
            'prise_en_charge': supplements['prise_en_charge']
        }
    }
    return estimation
