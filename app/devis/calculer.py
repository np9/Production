import pandas as pd
import app.devis.calcul_distance as cd
import app.devis.tarif as tt
from datetime import datetime


def heures_tariff(demande):
    categorie=demande['categorie']
    
    if categorie=='particulier':
       	return  pd.read_csv('app/devis/data/tarifs.csv', encoding='utf8')
    
    else: 
       	return pd.read_csv('app/devis/data/tarifs-pro.csv', encoding='utf8')
      
def suppf(demande):
    categorie=demande['categorie']
    
    if categorie=='particulier':       
      return  pd.read_csv('app/devis/data/supplements.csv', encoding='utf8')
    
    else:         
      return pd.read_csv('app/devis/data/supplements-pro.csv', encoding='utf8')


def tarifs(demande):
    
    supp = suppf(demande)
    heures_tarif = heures_tariff(demande)

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
        #tout le trajet en jour ou en nuit
        ligne = heures_tarif[heures_tarif['Type_Tarif'] == tt.type_tarif(demande)[0]]
        prix = float(ligne['tarif_par_km'])
    else:
        #trajet en partie en jour et en nuit
        ligne = heures_tarif[heures_tarif['Type_Tarif'] == tt.type_tarif(demande)[2][0]]#tarif nuit
        ligne2 = heures_tarif[heures_tarif['Type_Tarif'] == tt.type_tarif(demande)[2][1]]#tarif jour
        prix = float(ligne['tarif_par_km']) * tt.type_tarif(demande)[1][0] + float(ligne2['tarif_par_km']) * tt.type_tarif(demande)[1][1] #avec pourcentage de jour et de nuit
    
   
    
    #On calcule les suppléments
    #On récupère les lignes selon les suppléments et leurs prix
    an = supp[supp['Supplements'] == 'Animal']
    bag = supp[supp['Supplements'] == 'Bagage']
    PerS = supp[supp['Supplements'] == 'PersonneSup']
    Gar = supp[supp['Supplements'] == 'Gare']
    Aer = supp[supp['Supplements'] == 'Aeroport']
    
    #On calcule les suppléments
    supplement = float(demande['bagage']) * float(bag['Prix']) + float(demande['animaux']) * 1
    
    if int(demande['nb_passagers']) > 4:
        supplement += (float(demande['nb_passagers'])-4) * float(PerS['Prix'])
    
    if demande['gare'] == 'True':
        supplement += float(Gar['Prix'])
		
    if demande['aeroport'] == 'True':
        supplement += float(Aer['Prix'])

    #On concatenne les adresses de départ et d'arrivée
    depart = demande['numero_dep'] + ' ' + demande['adresse_dep'] + ' ' + demande['cp_dep'] + ' ' + demande['ville_dep']
    arrive = demande['numero_arr'] + ' ' + demande['adresse_arr'] + ' ' + demande['cp_arr'] + ' ' + demande['ville_arr']       

    #On calcule le prix total
    if demande['A-R'] == 'True':
        prixTotal = float(prise_en_charge['Prix']) + prix *( cd.recup_distance(cd.distance(depart,arrive)) + cd.recup_distance(cd.distance(arrive,depart)) ) + supplement
    else:
        prixTotal = float(prise_en_charge['Prix']) + prix * cd.recup_distance(cd.distance(depart,arrive)) + supplement

    
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
                'Nombre_km' : cd.recup_distance(cd.distance(depart,arrive)),
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
    

#print("Votre itinéraire devrait vous coûter " + str(calcul_tarifs(tt.demande)) + "€")
