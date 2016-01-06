from app import db
from app import app
from app import modeles
from sqlalchemy import create_engine
import contextlib
import sqlalchemy.exc
import glob

# Création de la base de données

uri = app.config['SQLALCHEMY_DATABASE_URI'].split('/')
url = '/'.join(uri[:-1])
bd = uri[-1]

with contextlib.suppress(sqlalchemy.exc.ProgrammingError):
    with create_engine(url,
                       isolation_level='AUTOCOMMIT').connect() as connexion:
        connexion.execute(
            "CREATE DATABASE {} WITH encoding='utf-8'".format(bd))

print('Base de données créée.')

# Création des tables

db.session.execute("SET client_encoding='utf-8'")
db.session.execute('CREATE EXTENSION postgis')
db.session.commit()
db.create_all()

print('Tables créées.')

# Création des triggers

# for trigger in glob.glob('app/triggers/*.sql'):
#	sql = open(trigger).read()
#	try:
#		db.session.execute(sql)
#		db.session.commit()
#	except:
#		print('Erreur sur le trigger {}.'.format(trigger))

# print('Triggers crées.')
