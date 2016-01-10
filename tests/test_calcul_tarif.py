from datetime import datetime, timedelta
from app.devis import tarif
from app.outils import utile


'''
Il faut que vous preniez en compte le fait que le Groupe 3
renvoit une adresse entière et non pas des morceaux d'adresse,
allez leur en parler. De plus, ils sont censés vous
renvoyer des chiffres, pas des chaînes de caractères.
Il vaut mieux séparer chaque test dans une fonction à part,
ca améliore la visibilité. Il n'y a plus besoin
de considérer les retours. Vous n'êtes pas obligés
de tout comparer dans vos tests, par exemple dans le
premier test c'est seulement le prix total qui nous
intéresse. 

La première fonction ci-dessous est un bon exemple.
'''

tarifs = utile.lire_json('app/devis/data/tarifs.json')
supplements = utile.lire_json('app/devis/data/supplements.json')

def tarif_minimum():
    '''
    On vérifie qu'un trajet court a bien comme prix
    le tarif minimum.
    '''
    # Choisir une date le lendemain du jour actuel
    date_debut = datetime.now() + timedelta(days=1)
    demande = {
        'commentaire': '',
        'adresse_dep': '10 Rue Elvire Toulouse',
        'adresse_arr': '17 Rue Elvire Toulouse',
        'categorie': 'particulier',
        'nb_passagers': 3,
        'adresse_arr': 'Rue Elvire',
        'date_debut': date_debut.isoformat(),
        'heures': 10,
        'minutes': 40,
        'paiement': 'especes',
        'bagages': 0,
        'animaux': 0,
        'gare': False,
        'aeroport': False
    }
    estimation = tarif.estimation(demande)
    assert estimation['prix']['total'] == supplements['tarif_minimum']


# def test_tarif():
# #Moins de 7€, tarif normal, avec bagage
#     demande = {
#          'minutes': '40',
#          'commentaire': '',
#          'heures': '08',
#          'cp_arr': '',
#          'numero_dep': '10',
#          'categorie': 'particulier',
#          'ville_dep': 'Toulouse',
#          'adresse_dep': 'Rue Elvire',
#          'ville_arr': 'Toulouse',
#          'nb_passagers': '3',
#          'cp_dep': '31400',
#          'numero_arr': '17',
#          'adresse_arr': 'Rue Elvire',
#          'date_debut': '2016-01-08',
#          'paiement': 'especes',
#          'bagage':'1',
#          'animaux':'0',
#          'gare':'False',
#          'aeroport':'False',
#          'A-R':'False',
#          'heure_retour':'12',
#          'minute_retour':'00'
#     }
#     resultat = {
#         'Gare': 'False',
#         'Prix_par_personnes_sup': '1.8',
#         'Prix_Total': '7.0',
#         'prix_total_animal': '0.0',
#         'prix_total_bagage': '0.95',
#         'Prix_Aeroport': '0',
#         'Prix_par_km': 1.62,
#         'prix_animal': '1.0',
#         'Prix_1_bagage': '0.95',
#         'Nombres_personnes_sup': 0,
#         'Prix_Gare': '0',
#         'animal': '0',
#         'Prix_personnes_sup': '0.0',
#         'Aeroport': 'False',
#         'Nombre_bagage': '1',
#         'Prise_en_charge': '1.9',
#         'Nombre_km': 0.03}
#     assert calculer.estimation(demande) == resultat

# #    #Moins de 7€, tarif normal, avec animal 
#     demande = {
#          'minutes': '40',
#          'commentaire': '',
#          'heures': '08',
#          'cp_arr': '',
#          'numero_dep': '10',
#          'categorie': 'particulier',
#          'ville_dep': 'Toulouse',
#          'adresse_dep': 'Rue Elvire',
#          'ville_arr': 'Toulouse',
#          'nb_passagers': '3',
#          'cp_dep': '31400',
#          'numero_arr': '17',
#          'adresse_arr': 'Rue Elvire',
#          'date_debut': '2016-01-08',
#          'paiement': 'especes',
#          'bagage':'0',
#          'animaux':'1',
#          'gare':'False',
#          'aeroport':'False',
#          'A-R':'False',
#          'heure_retour':'12',
#          'minute_retour':'00'
#     }
#     resultat = {
#         'Gare': 'False',
#         'Prix_par_personnes_sup': '1.8',
#         'Prix_Total': '7.0',
#         'prix_total_animal': '1.0',
#         'prix_total_bagage': '0.0',
#         'Prix_Aeroport': '0',
#         'Prix_par_km': 1.62,
#         'prix_animal': '1.0',
#         'Prix_1_bagage': '0.95',
#         'Nombres_personnes_sup': 0,
#         'Prix_Gare': '0',
#         'animal': '1',
#         'Prix_personnes_sup': '0.0',
#         'Aeroport': 'False',
#         'Nombre_bagage': '0',
#         'Prise_en_charge': '1.9',
#         'Nombre_km': 0.03}
#     assert calculer.estimation(demande) == resultat

#     #Moins de 7€, tarif normal, avec 2 personnes supplémentaires 
#     demande = {
#          'minutes': '40',
#          'commentaire': '',
#          'heures': '08',
#          'cp_arr': '',
#          'numero_dep': '10',
#          'categorie': 'particulier',
#          'ville_dep': 'Toulouse',
#          'adresse_dep': 'Rue Elvire',
#          'ville_arr': 'Toulouse',
#          'nb_passagers': '6',
#          'cp_dep': '31400',
#          'numero_arr': '17',
#          'adresse_arr': 'Rue Elvire',
#          'date_debut': '2016-01-08',
#          'paiement': 'especes',
#          'bagage':'0',
#          'animaux':'0',
#          'gare':'False',
#          'aeroport':'False',
#          'A-R':'False',
#          'heure_retour':'12',
#          'minute_retour':'00'
#     }
#     resultat = {
#         'Gare': 'False',
#         'Prix_par_personnes_sup': '1.8',
#         'Prix_Total': '7.0',
#         'prix_total_animal': '0.0',
#         'prix_total_bagage': '0.0',
#         'Prix_Aeroport': '0',
#         'Prix_par_km': 1.62,
#         'prix_animal': '1.0',
#         'Prix_1_bagage': '0.95',
#         'Nombres_personnes_sup': 2,
#         'Prix_Gare': '0',
#         'animal': '0',
#         'Prix_personnes_sup': '3.6',
#         'Aeroport': 'False',
#         'Nombre_bagage': '0',
#         'Prise_en_charge': '1.9',
#         'Nombre_km': 0.03}
#     assert calculer.estimation(demande) == resultat
    
#     #Moins de 7€, tarif normal, supplément gare
#     demande = {
#          'minutes': '40',
#          'commentaire': '',
#          'heures': '08',
#          'cp_arr': '',
#          'numero_dep': '10',
#          'categorie': 'particulier',
#          'ville_dep': 'Toulouse',
#          'adresse_dep': 'Rue Elvire',
#          'ville_arr': 'Toulouse',
#          'nb_passagers': '3',
#          'cp_dep': '31400',
#          'numero_arr': '17',
#          'adresse_arr': 'Rue Elvire',
#          'date_debut': '2016-01-08',
#          'paiement': 'especes',
#          'bagage':'0',
#          'animaux':'0',
#          'gare':'True',
#          'aeroport':'False',
#          'A-R':'False',
#          'heure_retour':'12',
#          'minute_retour':'00'
#     }
#     resultat = {
#         'Gare': 'True',
#         'Prix_par_personnes_sup': '1.8',
#         'Prix_Total': '7.0',
#         'prix_total_animal': '0.0',
#         'prix_total_bagage': '0.0',
#         'Prix_Aeroport': '0',
#         'Prix_par_km': 1.62,
#         'prix_animal': '1.0',
#         'Prix_1_bagage': '0.95',
#         'Nombres_personnes_sup': 0,
#         'Prix_Gare': '0.85',
#         'animal': '0',
#         'Prix_personnes_sup': '0.0',
#         'Aeroport': 'False',
#         'Nombre_bagage': '0',
#         'Prise_en_charge': '1.9',
#         'Nombre_km': 0.03}
#     assert calculer.estimation(demande) == resultat
    
#     #Moins de 7€, tarif normal, supplément aeroport
#     demande = {
#          'minutes': '40',
#          'commentaire': '',
#          'heures': '08',
#          'cp_arr': '',
#          'numero_dep': '10',
#          'categorie': 'particulier',
#          'ville_dep': 'Toulouse',
#          'adresse_dep': 'Rue Elvire',
#          'ville_arr': 'Toulouse',
#          'nb_passagers': '3',
#          'cp_dep': '31400',
#          'numero_arr': '17',
#          'adresse_arr': 'Rue Elvire',
#          'date_debut': '2016-01-08',
#          'paiement': 'especes',
#          'bagage':'0',
#          'animaux':'0',
#          'gare':'False',
#          'aeroport':'True',
#          'A-R':'False',
#          'heure_retour':'12',
#          'minute_retour':'00'
#     }
#     resultat = {
#         'Gare': 'False',
#         'Prix_par_personnes_sup': '1.8',
#         'Prix_Total': '7.0',
#         'prix_total_animal': '0.0',
#         'prix_total_bagage': '0.0',
#         'Prix_Aeroport': '2.25',
#         'Prix_par_km': 1.62,
#         'prix_animal': '1.0',
#         'Prix_1_bagage': '0.95',
#         'Nombres_personnes_sup': 0,
#         'Prix_Gare': '0',
#         'animal': '0',
#         'Prix_personnes_sup': '0.0',
#         'Aeroport': 'True',
#         'Nombre_bagage': '0',
#         'Prise_en_charge': '1.9',
#         'Nombre_km': 0.03}
#     assert calculer.estimation(demande) == resultat
    
#         #Moins de 7€, tarif nuit/jour ferie/dimanche, sans supplément  
#     demande = {
#          'minutes': '40',
#          'commentaire': '',
#          'heures': '08',
#          'cp_arr': '',
#          'numero_dep': '10',
#          'categorie': 'particulier',
#          'ville_dep': 'Toulouse',
#          'adresse_dep': 'Rue Elvire',
#          'ville_arr': 'Toulouse',
#          'nb_passagers': '3',
#          'cp_dep': '31400',
#          'numero_arr': '17',
#          'adresse_arr': 'Rue Elvire',
#          'date_debut': '2017-01-01',
#          'paiement': 'especes',
#          'bagage':'0',
#          'animaux':'0',
#          'gare':'False',
#          'aeroport':'False',
#          'A-R':'False',
#          'heure_retour':'12',
#          'minute_retour':'00'
#     }
#     resultat = {
#         'Gare': 'False',
#         'Prix_par_personnes_sup': '1.8',
#         'Prix_Total': '7.0',
#         'prix_total_animal': '0.0',
#         'prix_total_bagage': '0.0',
#         'Prix_Aeroport': '0',
#         'Prix_par_km': 2.24,
#         'prix_animal': '1.0',
#         'Prix_1_bagage': '0.95',
#         'Nombres_personnes_sup': 0,
#         'Prix_Gare': '0',
#         'animal': '0',
#         'Prix_personnes_sup': '0.0',
#         'Aeroport': 'False',
#         'Nombre_bagage': '0',
#         'Prise_en_charge': '1.9',
#         'Nombre_km': 0.03}
#     assert calculer.estimation(demande) == resultat

#         #Plus de 7€, tarif normal, sans supplément
#     demande = {
#          'minutes': '40',
#          'commentaire': '',
#          'heures': '08',
#          'cp_arr': '31500',
#          'numero_dep': '10',
#          'categorie': 'particulier',
#          'ville_dep': 'Toulouse',
#          'adresse_dep': 'Rue Elvire',
#          'ville_arr': 'Toulouse',
#          'nb_passagers': '3',
#          'cp_dep': '31400',
#          'numero_arr': '',
#          'adresse_arr': 'Avenue jean gonord',
#          'date_debut': '2016-01-08',
#          'paiement': 'especes',
#          'bagage':'0',
#          'animaux':'0',
#          'gare':'False',
#          'aeroport':'False',
#          'A-R':'False',
#          'heure_retour':'12',
#          'minute_retour':'00'
#     }
#     resultat = {
#         'Gare': 'False',
#         'Prix_par_personnes_sup': '1.8',
#         'Prix_Total': '10.42',
#         'prix_total_animal': '0.0',
#         'prix_total_bagage': '0.0',
#         'Prix_Aeroport': '0',
#         'Prix_par_km': 1.62,
#         'prix_animal': '1.0',
#         'Prix_1_bagage': '0.95',
#         'Nombres_personnes_sup': 0,
#         'Prix_Gare': '0',
#         'animal': '0',
#         'Prix_personnes_sup': '0.0',
#         'Aeroport': 'False',
#         'Nombre_bagage': '0',
#         'Prise_en_charge': '1.9',
#         'Nombre_km': 5.26}
#     assert calculer.estimation(demande) == resultat
