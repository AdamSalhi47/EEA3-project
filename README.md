# CineTrack — Gestionnaire Intelligent de Séries TV

**CineTrack** permet de rechercher automatiquement les informations d'une série TV (genre, année, note moyenne) via une API publique et de gérer sa watchlist personnelle avec suivi de visionnage et sauvegarde locale.

## API utilisée
- **TVMaze API** (`https://api.tvmaze.com/singlesearch/shows?q={titre}`)
- **Avantages** : 100 % gratuite, **aucune clé API requise**, réponses JSON rapides et structurées.

## Architecture du projet (3 modules)
- `donnees.py` : lecture et écriture des données locales (`series.json` par défaut + export/import `series.csv`).
- `api.py` : interrogation de l'API REST TVMaze et gestion des erreurs réseau/HTTP.
- `produit.py` : interface menu en ligne de commande reliant `api.py` et `donnees.py`, avec cache anti-doublons et statistiques.

## Installation
```bash
pip install requests
```

## Utilisation
```bash
python produit.py
```

## Équipe (TIC / EEA — ECUEF132)
- **Membre 1** : module `donnees.py` (persistance JSON/CSV)
- **Membre 2** : module `api.py` (requêtes REST TVMaze & gestion d'erreurs)
- **Membre 3** : module `produit.py` (menu interactif, statistiques & intégration)
