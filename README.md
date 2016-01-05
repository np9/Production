# Production

Ce dossier contient l'application finale, celle qui doit marcher sans faille.

## Architecture

A faire.

## Utilisation

Il faut d'abord s'assurer que les valeurs dans ``config.py`` soient cohérentes, c'est à dire bien faire en sorte que le port et le mot de passe de PostgreSQL soient les mêmes que ceux de l'ordinateur d'où l'application est lancée. Si la base de données a déjà été créée elle peut être supprimée en lancant le script ``suppression.py``.

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

Il faut utiliser l'utilitaire ``ngrok`` qui est inclu dans le dossier. Commencez par taper ``python run.py`` dans une console. Ensuite ouvrez une nouvelle console puis tapez ``./ngrok http 5000``, ``ngrok`` vous informe alors de l'URL à laquelle le localhost est disponible.

## Déploiement sur un serveur

Se référer au dossier ``setup/``.
