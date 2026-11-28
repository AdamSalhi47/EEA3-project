"""donnees.py — Sauvegarde et chargement JSON / CSV pour CineTrack."""

import csv
import json
import os

DOSSIER_APP = os.path.dirname(os.path.abspath(__file__))
FICHIER_JSON = os.path.join(DOSSIER_APP, "series.json")
FICHIER_CSV = os.path.join(DOSSIER_APP, "series.csv")
CHAMPS = ["titre", "genre", "annee", "note", "statut"]


def charger(fichier_json=FICHIER_JSON):
    """Charge la liste des séries depuis series.json (liste vide si absent)."""
    try:
        with open(fichier_json, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []


def sauvegarder(series, fichier_json=FICHIER_JSON):
    """Enregistre la liste des séries dans series.json."""
    with open(fichier_json, "w", encoding="utf-8") as f:
        json.dump(series, f, ensure_ascii=False, indent=2)


def exporter_csv(series, fichier_csv=FICHIER_CSV):
    """Exporte la liste des séries vers series.csv."""
    with open(fichier_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CHAMPS)
        writer.writeheader()
        for s in series:
            writer.writerow({k: s.get(k, "") for k in CHAMPS})


def importer_csv(fichier_csv=FICHIER_CSV):
    """Importe la liste des séries depuis series.csv."""
    try:
        series = []
        with open(fichier_csv, "r", newline="", encoding="utf-8") as f:
            for ligne in csv.DictReader(f):
                titre = str(ligne.get("titre", "")).strip()
                if not titre:
                    continue
                try:
                    annee = int(str(ligne.get("annee", 0)).strip())
                except ValueError:
                    annee = 0
                try:
                    note = float(str(ligne.get("note", 0.0)).strip())
                except ValueError:
                    note = 0.0
                series.append({
                    "titre": titre,
                    "genre": str(ligne.get("genre", "")).strip() or "Non classé",
                    "annee": annee,
                    "note": note,
                    "statut": str(ligne.get("statut", "")).strip() or "À voir",
                })
        return series
    except (FileNotFoundError, OSError):
        return []
