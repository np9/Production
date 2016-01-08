# -*- coding: utf-8 -*-
"""
@author: Groupe 6
Objectif : Différentes fonctions permettant de récupérer des informations 
sur la course.
Last Upate : 8/01/2016 13:00
"""

from app import db

def information_course(numero):
    ''' Récupère des informations sur la course passée en paramètre '''

    # Création de la requete de selection des conducteurs
    query = '''SELECT places, animaux, animaux_grands
            FROM  Courses
            WHERE numero = {numero_course} ;'''         

    # Création et execution de la requête parametrée
    query_param = query.format(numero_course=numero)
    result = db.engine.execute(query_param).fetchall()  
   
    # Création du dictionnare contenant les informations 
    course = {}
    course['numero']  =  numero 
    course['places']  =  result[0][0] 
    course['animaux_petit']  =  result[0][1]  
    course['animaux_gros']  =  result[0][2] 
    
    
    return course
    