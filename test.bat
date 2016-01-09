:: On installe les packages nécessaire
pip install -r requirements.txt
:: On supprime l'ancienne BD
python suppression.py
:: On crée la BD
python creation.py
:: On remplit la BD
python insertions.py
:: On lance les tests
nosetests
:: On lance l'application
python run.py