# Production

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

## Partage du localhost

Il faut utiliser l'utilitaire ``ngrok``. Celui-ci est téléchargeable [ici](https://ngrok.com/download). Commencez pas dézipper le téléchargement et à inclure le binaire qui s'appelle ``ngrok`` à la racine. Tapez ensuite ``python run.py`` dans une console. Puis ouvrez une nouvelle console puis tapez ``./ngrok http 5000``, ``ngrok`` vous informe alors de l'URL à laquelle le localhost est disponible.

## Déploiement sur un serveur

Se référer au dossier ``setup/``.

## Installation de packages

### Installer geoalchemy2

```sh
# Installer la librairie
pip install geoalchemy2
```
### Installer shapely

#### Linux

```sh
sudo apt-get build-dep python-shapely
# OU
brew install python-shapely
```

#### Windows
  
Téléchargez la librairie ``shapely`` sur [ce site](http://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely) puis mettez la dans le dossier de votre projet (exemple : TAXISID)

```sh
# Se placer dans le dossier où se trouve le fichier
pip install nomdufichier.whl
```

#### MacOS

```sh
# Installer Homebrew
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
# Installer Geos
brew install geos
# Installer Shapely
pip install shapely
```
