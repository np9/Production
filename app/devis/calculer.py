import pandas as pd
import app.devis.tarif as tt
import app.outils.geographie as geo
from datetime import datetime
from app.calcul.distance import Parcours as Par


def tarifs(demande):
    
    supp = pd.read_csv('app/devis/data/supplements.csv', encoding='utf8')
    heures_tarif = pd.read_csv('app/devis/data/tarifs.csv', encoding='utf8')

    #On initialise les prix de départ et les suppléments
    prise_en_charge = supp[supp['Supplements'] == 'Prise_en_charge']
    
    #On récupère la date et l'heure de départ
    date = demande['date_debut'].split('-')
    annee = int(date[0])
    mois = int(date[1])
    jour = int(date[2])
    heure = int(demande['heures'])
    minutes = int(demande['minutes'])
    
    #Mise en forme de la date
    date = datetime(
        annee,
        mois,
        jour,
        heure,
        minutes
    )

 #On prend les lignes selon les types de tarifs et on en tire le prix associé
    if tt.type_tarif(demande)[1] == [0,1] or tt.type_tarif(demande)[1] == [1,0]:
        #Tout le trajet en jour ou en nuit
        ligne = heures_tarif[heures_tarif['Type_Tarif'] == tt.type_tarif(demande)[0]]
        prix = float(ligne['tarif_par_km'])
    else:
        #Trajet en partie en jour et en nuit
        #Récupération du tarif de nuit
        ligne = heures_tarif[heures_tarif['Type_Tarif'] == tt.type_tarif(demande)[2][0]]
        #Récupération du tarif de jour
        ligne2 = heures_tarif[heures_tarif['Type_Tarif'] == tt.type_tarif(demande)[2][1]]
        #Calcul du prix/km par pourcentage du temps passé en tarif jour et nuit
        prix = float(ligne['tarif_par_km']) * tt.type_tarif(demande)[1][0] + float(ligne2['tarif_par_km']) * tt.type_tarif(demande)[1][1] #avec pourcentage de jour et de nuit
       
    #Calcul des suppléments
    #On récupère les lignes selon les suppléments et leurs prix
    an= supp[supp['Supplements'] == 'Animal']
    bag = supp[supp['Supplements'] == 'Bagage']
    PerS = supp[supp['Supplements'] == 'PersonneSup']
    Gar = supp[supp['Supplements'] == 'Gare']
    Aer = supp[supp['Supplements'] == 'Aeroport']
    
    #Calcul du montant total des suppléments
    #Suppléments pour bagages et/ou animaux
    supplement = float(demande['bagage']) * float(bag['Prix']) + float(demande['animaux']) * 1
    
    #Suppléments pour un passager supplémentaire
    if int(demande['nb_passagers']) > 4:
        supplement += (float(demande['nb_passagers'])-4) * float(PerS['Prix'])
    
    #Suppléments pour la prise en charge à la gare
    if demande['gare'] == 'True':
        supplement += float(Gar['Prix'])
	
    #Suppléments pour la prise en charge à l'aéroport	
    if demande['aeroport'] == 'True':
        supplement += float(Aer['Prix'])

    #On concatenne les adresses de départ et d'arrivée
    depart = demande['numero_dep'] + ' ' + demande['adresse_dep'] + ' ' + demande['cp_dep'] + ' ' + demande['ville_dep']
    arrive = demande['numero_arr'] + ' ' + demande['adresse_arr'] + ' ' + demande['cp_arr'] + ' ' + demande['ville_arr']       

    #On calcule le prix total
    # prix = coût de prise en charge + tarif par km * nombre de km + coût des suppléments 
    prixTotal = float(prise_en_charge['Prix']) + prix * round(float(Par(geo.geocoder(depart),geo.geocoder(arrive),str(date)).distance),2) + supplement
          
    #On vérifie que le prix total soit supérieur au prix minimal
    prixMinimal = float(supp[supp['Supplements'] == 'Tarif_minimum']['Prix'])
    
    if prixTotal < prixMinimal:
        prixTotal = prixMinimal
    
#On retourne le prix total via un dictionnaire de données
#Gestion des conditions

    #Si le client est pris à l'aéroport
    if demande['aeroport'] == 'True':   
        prixA = float(Aer['Prix'])
    else:
        prixA = 0
        
    #Si le nombre de personne est supérieur à 4
    if int(demande['nb_passagers']) > 4:
        nbPersonnes =  float(demande['nb_passagers']) - 4
    else:
        nbPersonnes = 0
   
     #Si le client est pris à la gare
    if demande['gare'] == 'True':
        prixG = float(Gar['Prix'])
    else:
        prixG = 0
                

    dico = {
                'Prix_Total' : str(round(prixTotal,2)), 
                'Prise_en_charge' : str(float(prise_en_charge['Prix'])),
                'Prix_par_km' : prix,
                'Nombre_km' : Par(geo.geocoder(depart),geo.geocoder(arrive),str(date)).distance,
                'Nombre_bagage' : str(demande['bagage']),
                'Prix_1_bagage' : str(float(bag['Prix'])),
                'prix_total_bagage' : str(float(demande['bagage']) * float(bag['Prix'])),
                'animal' : str(demande['animaux']),
                'prix_animal' : str(float(an['Prix'])),
                'prix_total_animal' : str(float(demande['animaux']) * float(an['Prix'])),
                'Gare' : str(demande['gare']),
                'Prix_Gare' : str(prixG),
                'Nombres_personnes_sup' : nbPersonnes,
                'Prix_par_personnes_sup' : str(float(PerS['Prix'])),
                'Prix_personnes_sup' : str((nbPersonnes) * float(PerS['Prix'])),
                'Aeroport' : str(demande['aeroport']),
                'Prix_Aeroport':str(prixA)
                }

    #On retourne le prix total
    return dico    
    
