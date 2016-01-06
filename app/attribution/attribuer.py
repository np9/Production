from sqlalchemy.sql import text
from app import db
        

def conducteurs_dispos(pnum):
    ''' On crée une fonction qui permet d'afficher les conducteurs 
    disponibles. '''
    # On va récuperer les données dans la BD 
    sql = '''
        SELECT telephone 
        FROM conducteurs cd
        WHERE cd.libre = TRUE;
    '''
        
    # On récupère les lignes qui résultent de la requête
    requete = db.engine.execute(text(sql))
    lignes = requete.fetchall()
    return lignes
