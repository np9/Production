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
    supplement += max(0, int(demande['nb_passagers']) - 4) * supplements['personne_sup']
    # Trajet à vide (ça ne m'a pas l'air bon, à discuter)
    supplement += supplements['trajet_a_vide']
    # Prise en charge à la gare
    if demande['gare'] is True:
        supplement += supplements['gare']
    # Prise en charge à l'aéroport
    if demande['aeroport'] is True:
        supplement += supplements['aeroport']


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

    # Prix du trajet à vide
    tav = supplements['trajet_a_vide']

    # Calculer le supplément
    supplement = calculer_supplement(demande, supplements)

    # Tarif supplémentaire appliqué à un trajet ralenti (si temps de trajet plus long de 5 minutes 
    # par rapport à temps de trajet de référence, on applique une nouvelle tarification par minute de trajet supplémentaire)

    if round(simulation['ecart']/60) > 5:
        diff_minutes = round(simulation['ecart']/60) - 5
    else:
        diff_minutes = 0

    estimation = diff_minutes * supplements['prix_trajet_ralenti']/60



    # Calcul du total minimum estimé
    total = montant + supplement + tav + estimation
    # Prise en compte du tarif minimum
    total = max(total, supplements['tarif_minimum'])


    # On retourne l'estimation à travers un dictionnaire de données

    estimation = {
        'prix': {
            'montant': round(montant, 2),
            'supplement': round(supplement, 2),
            'trajet_a_vide' : tav,
            'total_min': round(total)

        },
        'detail': {
            'parcours': {
                'duree': str(duree),
                'distance': round(distance,1),
                'prix_par_km': prix_par_km
            },
            'bagages': {
                'nb': demande['bagages'],
                'prix': supplements['bagage'],
                'total': int(demande['bagages']) * supplements['bagage']
            },
            'animaux': {
                'nb': demande['animaux'],
                'prix': supplements['animal'],
                'total': int(demande['animaux']) * supplements['animal']
            },
            'personnes': {
                'nb': demande['nb_passagers'],
                'supplementaires': {
                    'nb': max(0, int(demande['nb_passagers']) - 4),
                    'prix': supplements['personne_sup'],
                    'total': max(0, int(demande['nb_passagers']) - 4) * supplements['personne_sup']
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
