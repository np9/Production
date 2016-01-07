# TaxiSID

Ce dossier contient l'application finale, celle qui doit marcher sans faille.


## Architecture

![alt text](doc/architecture.png)


## Utilisation

Il faut d'abord s'assurer que les valeurs dans ``config.py`` soient cohérentes :
- ligne 9 : le mot de passe de PostgreSQL doit être le même que ceux de l'ordinateur d'où l'application est lancée
- ligne 10 : le port doit être le même ce celui d'où l'application est lancée

Si la base de données a déjà été créée elle peut être supprimée en lancant le script ``suppression.py``.

```sh
# Installer les librairies
pip install -r requirements.txt
# Créer la base de données
python creation.py
# Insérer les données de départ
python insertions.py
# Lancer le site web
python run.py
```

Ensuite il suffit de consulter l'URL ``localhost:5000`` dans le navigateur.

#### Partage du localhost

Il faut utiliser l'utilitaire ``ngrok``. Celui-ci est téléchargeable [ici](https://ngrok.com/download). Commencez pas dézipper le téléchargement et à inclure le binaire qui s'appelle ``ngrok`` à la racine. Tapez ensuite ``python run.py`` dans une console. Puis ouvrez une nouvelle console puis tapez ``./ngrok http 5000``, ``ngrok`` vous informe alors de l'URL à laquelle le localhost est disponible.

#### Déploiement sur un serveur

Se référer au dossier ``setup/``.


## Motivation

Ce projet a été proposé par la société CapitoleTaxi. Notre équipe a pour but de créer une application web et téléphone. Celle ci doit permettre à des utilisateurs de réserver un taxi et doit permettre aux taxis d'accepter ou non les courses qu'on leur propose. Une demande de course doit être proposé aux taxis les plus proches de l'adresse de départ de l'utilisateur.


## Installation de packages

#### Installer geoalchemy2

```sh
# Installer la librairie
pip install geoalchemy2
```
#### Installer shapely

##### Sur Linux

```sh
sudo apt-get build-dep python-shapely
# OU
brew install python-shapely
```

##### Sur Windows
  
Téléchargez la librairie ``shapely`` sur [ce site](http://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely) puis mettez la dans le dossier de votre projet (exemple : TAXISID)

```sh
# Se placer dans le dossier où se trouve le fichier
pip install nomdufichier.whl
```

##### Sur MacOS

```sh
# Installer Homebrew
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
# Installer Geos
brew install geos
# Installer Shapely
pip install shapely
```

#### Installer psycopg2

##### Sur Windows et Linux

Téléchargez la librairie ``psycopg2`` [ici](http://www.lfd.uci.edu/~gohlke/pythonlibs/#psycopg) puis le mettre à la racine du projet.

```sh
# Installer psycopg2
pip install psycopg2
```

Attention vous pouvez avoir une erreur psycopg2 si vous n'avez pas mis votre mot de passe postgre dans le fichier config.py, voir la partie utilisation ci-dessus.

##### Sur Mac

Il faut d'abord indiquer le chemin vers l'exécutable de PostgreSQL, installer ``psycopg2`` via ``pip`` et enfin changer la librairie /usr/lib/libpq.5.dylib car elle est trop vieille avec les commandes suivantes:

```sh
export PATH="/Library/PostgreSQL/9.5/bin:$PATH"
anaconda/bin/pip install psycopg2
sudo mv /usr/lib/libpq.5.dylib /usr/lib/libpq.5.dylib.old
sudo ln -s /Library/PostgreSQL/9.5/lib/libpq.5.dylib /usr/lib
```

Si vous avez OS X El Capitan, que les commandes précédentes ne fonctionnent pas ou que vous avez un message d'erreur en important ``psycopg2`` dans Python, veuillez suivre les consignes suivantes :

```sh
anaconda/bin/pip install psycopg2
sudo chown -R $(whoami):admin /usr/local
sudo ln -s /Library/PostgreSQL/9.5/lib/libssl.1.0.0.dylib /usr/local/lib/
sudo ln -s /Library/PostgreSQL/9.5/lib/libcrypto.1.0.0.dylib /usr/local/lib/
```

Puis installer psycopg2

```sh
pip install psycopg2
```


## API

L'API renvoit des données au format json, le lien vers celle ci est : http://localhost:5000/api

Les différentes commandes sont :
- ~/api/utilisateurs
- ~/api/conducteurs
- ~/api/adresses
- ~/api/stations
- ~/api/vehicules
- ~/api/courses
- ~/api/factures
- ~/api/positions


## Contributeurs

Ce projet est réalisé par tous les élèves de la formation CMI SID de Toulouse [site de la formation](https://cmisid.univ-tlse3.fr/) de l'Université Paul Sabatier, avec l'aide de certains de leurs professeurs.
