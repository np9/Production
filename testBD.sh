#!/bin/sh

# on installe les packages nécessaire
pip install -r requirements.txt
# on supprime l'ancienne BD
python suppression.py
# on crée la BD
python creation.py
# on rempli la BD
python insertions.py
# on fait les tests
py.test
# on lance l'application
python run.py
