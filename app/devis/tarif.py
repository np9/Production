from datetime import datetime

#On cherche à retourner le type de tarif (Jour ou Nuit/Dimanche/JoursFériés)
def type_tarif(demande):
    
    #On récupère la date et l'heure de départ
    date = demande['date_debut'].split('-')
    annee_depart = int(date[0])
    mois_depart = int(date[1])
    jour_depart = int(date[2])
    heure_depart = int(demande['heures'])
    minutes_depart = int(demande['minutes'])
    
    #Mise en forme de la date
    date = datetime(
        annee_depart,
        mois_depart,
        jour_depart,
        heure_depart,
        minutes_depart
    )

    #Recherche du tarif: Jour ou Nuit/JourFerie/Dimanche    
    #Initialisation du booléen
    test = False
    
    #On concaténe le mois et le jour de façon a avoir une chaine de la forme 'jour/mois'  
    dateC = str(date.day)+ '/' +str(date.month)
    
    #On vérifie si la date en entrée est un jour ferie
    ferie = dateC in [
        '1/1',
        '1/5',
        '8/5',
        '14/7',
        '15/8',
        '1/11',
        '11/11',
        '25/12'
    ]+feries(date.year)
    
    #print(ferie)    
    
    #On vérifie si l'heure est de nuit ou un dimanche
    dimanche = date.weekday()
   
    if date.hour > 19:
        test = True
    
    elif date.hour < 8:
        test = True
    
    elif ferie == True or dimanche == 6:
        test = True  
        
    #Choix du tarif
    #Si Aller retour
    if demande['A-R'] == 'True':
    #Test tarif spécial (Nuit/JourFérié/Dimanche)
        if test:
            Type_tarif = 'TarifB'
    #Tarif de jour par défaut 
        else:
            Type_tarif = 'TarifA'
    #Si trajet simple
    else:
    #Test tarif spécial (Nuit/JourFérié/Dimanche)
        if test :
            Type_tarif = 'TarifD'
            
    #Tarif de jour par défaut 
        else:
            Type_tarif = 'TarifC'
            
    return Type_tarif

def feries(an):
    #on calcule les dates des jours fériés variables selon les années (lundi de paques, lundi de pentecote et jeudi de l'ascension)
    #Calcule la date de Pâques d'une année donnée an (=nombre entier)
    a=an//100
    b=an%100
    c=(3*(a+25))//4
    d=(3*(a+25))%4
    e=(8*(a+11))//25
    f=(5*a+b)%19
    g=(19*f+c-e)%30
    h=(f+11*g)//319
    j=(60*(5-d)+b)//4
    k=(60*(5-d)+b)%4
    m=(2*j-k-g+h)%7
    
    #à partir 
    #lundi de paques
    n2=(g-h+m+115)//31
    p2=(g-h+m+115)%31
    jourLundiPaques=p2+1
    moisLundiPaques=n2
    
    #lundi de pentecote
    n3=(g-h+m+165)//31
    p3=(g-h+m+165)%31
    jourLundiPentecote=p3+1
    moisLundiPentecote=n3
    
    #jeudi de l'ascension
    n4=(g-h+m+154)//31
    p4=(g-h+m+154)%31
    jourJeudiAscension=p4+1
    moisJeudiAscension=n4
    
    return [str(jourLundiPaques) + '/' + str(moisLundiPaques),str(jourLundiPentecote) + '/' + str(moisLundiPentecote),str(jourJeudiAscension) + '/' + str(moisJeudiAscension)]
    
