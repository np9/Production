from datetime import datetime, timedelta
import app.outils.geographie as geo
from app.calcul.distance import Parcours as Par

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
    date = datetime(annee_depart,mois_depart,jour_depart,heure_depart,minutes_depart)
    
    #On concatenne les adresses de départ et d'arrivée
    depart = demande['numero_dep'] + ' ' + demande['adresse_dep'] + ' ' + demande['cp_dep'] + ' ' + demande['ville_dep']
    arrive = demande['numero_arr'] + ' ' + demande['adresse_arr'] + ' ' + demande['cp_arr'] + ' ' + demande['ville_arr']       

    #Recherche du tarif: Jour ou Nuit/JourFerie/Dimanche    
    #On calcule la date d'arrivée estimée du trajet
    temps_trajet = timedelta(minutes=Par(geo.geocoder(depart),geo.geocoder(arrive),str(date)).temps)
    date_arrive = date + temps_trajet

    #On définit les limites de passages aux horaires jour et nuit
    date_lim_jour = datetime.strptime(str(annee_depart) + '-' + str(mois_depart) + '-' + str(jour_depart) + ' 08:00:00', '%Y-%m-%d %H:%M:%S')
    date_lim_soir = datetime.strptime(str(annee_depart) + '-' + str(mois_depart) + '-' + str(jour_depart) + ' 19:00:00', '%Y-%m-%d %H:%M:%S')

    #On calcule le pourcentage de temps passé avec chaque tarif (nuit/jour) lorsqu'il y a un changement de tarif en cours de trajet
    #Si le départ est avant 8h
    if date < date_lim_jour:
        #Si l'arrivée est entre 8h et 19h
        if date_arrive >= date_lim_jour and date_arrive < date_lim_soir:
            temps_nuit = (date_lim_jour - date)/temps_trajet
            temps_jour = (date_arrive - date_lim_jour)/temps_trajet
            intervalle = [round(temps_nuit,2), round(temps_jour,2)]
        #Si l'arrivée est après 19h
        elif date_arrive >= date_lim_soir:
            temps_nuit = ((date_lim_jour - date) + (date_arrive - date_lim_soir))/temps_trajet
            temps_jour = (date_lim_soir - date_lim_jour)/temps_trajet
            intervalle = [round(temps_nuit,2), round(temps_jour,2)]
        #Si le trajet est seulement de nuit
        else:
            intervalle = [1,0]
            Type_tarif = 'TarifD'
    #Si le départ est avant 19h
    elif date < date_lim_soir:
        #Si l'arrivée est après 19h et avant 8h le lendemain
        if date_arrive >= date_lim_soir and date_arrive < date_lim_jour + timedelta(days=1):
            temps_jour = (date_lim_soir - date)/temps_trajet
            temps_nuit = (date_arrive - date_lim_soir)/temps_trajet
            intervalle = [round(temps_nuit,2), round(temps_jour,2)]
        #Si l'arrivée est après 8h le lendemain
        elif date_arrive >= date_lim_jour + timedelta(days=1):
            temps_nuit = ((date_lim_jour + timedelta(days=1)) - date_lim_soir)/temps_trajet
            temps_jour = ((date_lim_soir - date) + (date_arrive - date_lim_jour + timedelta(days=1)))/temps_trajet
            intervalle = [round(temps_nuit,2), round(temps_jour,2)]
        #Si le trajet est seulement de jour
        elif date_arrive < date_lim_soir: 
            intervalle = [0,1]
            Type_tarif = 'TarifC'
    #Si le départ est après 19h
    elif date >= date_lim_soir:
        #Si l'arrivée est entre 8h et 19h le lendemain
        if date_arrive >= date_lim_jour + timedelta(days=1) and date_arrive < date_lim_soir + timedelta(days=1):
            temps_nuit = ((date_lim_jour + timedelta(days=1)) - date) / temps_trajet
            temps_jour = (date_arrive - date_lim_jour + timedelta(day=1))/temps_trajet
            intervalle = [round(temps_nuit,2), round(temps_jour,2)]
        #Si l'arrivée est après 19h le lendemain
        elif date_arrive >= date_lim_soir + timedelta(days=1):
            temps_nuit = (date + (date_lim_jour + timedelta(days=1)) + (date_arrive - (date_lim_soir + timedelta(days=1))))/temps_trajet
            temps_jour = ((date_lim_soir + timedelta(days=1)) - (date_lim_jour + timedelta(days=1)))/temps_trajet
            intervalle = [round(temps_nuit,2), round(temps_jour,2)]
        #Si le trajet est seulement de nuit
        else:
            intervalle = [1,0]
            Type_tarif = 'TarifD'
   
 
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
    
    #On vérifie si le jour est un dimanche
    dimanche = date.weekday()
   
    if ferie == True or dimanche == 6:
        intervalle = [1,0]
        Type_tarif = 'TarifD'
        
  #Initialise les tarifs à utiliser en cas de changement de tarifs en cours de trajet           
    double_tarif = ['TarifD','TarifC']
    
    return Type_tarif, intervalle, double_tarif

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
    
