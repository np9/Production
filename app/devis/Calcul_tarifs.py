import pandas as pd
import app.devis.calcul_distance as cd
import app.devis.Type_tarif as tt

heures_tarif = pd.read_csv('app/devis/data/tarifs.csv', encoding='utf8')
supp = pd.read_csv('app/devis/data/supplements.csv', encoding='utf8')

def calcul_tarifs(demande):
    
    #On initialise les prix de départ et les suppléments
    prise_en_charge = supp[supp['Supplements'] == 'Prise_en_charge']
    
    #On prend les lignes selon les types de tarifs et on en tire le prix associé
    ligne = heures_tarif[heures_tarif['Type_Tarif'] == tt.Type_tarif(demande)]
    prix = float(ligne['tarif_par_km'])
    
    #On calcule les suppléments
    #On récupère les lignes selon les suppléments et leurs prix
    bag = supp[supp['Supplements'] == 'Bagage']
    PerS = supp[supp['Supplements'] == 'PersonneSup']
    Gar = supp[supp['Supplements'] == 'Gare']
    
    #On calcule les suppléments
    supplement = float(demande['bagage']) * float(bag['Prix']) + float(demande['animaux']) * 1
    
    if int(demande['nb_passagers']) > 4:
        supplement += (float(demande['nb_passagers'])-4) * float(PerS['Prix'])
    
    if demande['gare'] == True:
        supplement += float(Gar['Prix'])

    #On concatenne les adresses de départ et d'arrivée
    depart = demande['numero_dep'] + ' ' + demande['adresse_dep'] + ' ' + demande['cp_dep'] + ' ' + demande['ville_dep']
    arrive = demande['numero_arr'] + ' ' + demande['adresse_arr'] + ' ' + demande['cp_arr'] + ' ' + demande['ville_arr']       

    #On calcule le prix total
    prixTotal = float(prise_en_charge['Prix']) + prix * cd.recup_distance(cd.distance(depart,arrive)) + supplement
    
    #On vérifie que le prix total soit supérieur au prix minimal
    prixMinimal = float(supp[supp['Supplements'] == 'Tarif_minimum']['Prix'])
    
    if prixTotal < prixMinimal:
        prixTotal = prixMinimal
        
    #On retourne le prix total
    return prixTotal
    
#print("Votre itinéraire devrait vous coûter " + str(round(calcul_tarifs(tt.demande),2)) + "€")

