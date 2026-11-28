"""donnees.py — Gestion de la persistance (JSON et CSV) pour CineTrack."""

import csv
import json

FICHIER_JSON = "series.json"
FICHIER_CSV = "series.csv"
CHAMPS = ["titre", "genre", "annee", "note", "statut"]


def charger(fichier_json=FICHIER_JSON):
    """Charge la liste des séries depuis un fichier JSON.
    Si le fichier n'existe pas encore (1er lancement) ou est corrompu,
    renvoie une liste vide sans planter.
    """
    try:
        with open(fichier_json, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []


def sauvegarder(series, fichier_json=FICHIER_JSON):
    """Enregistre la liste des séries dans un fichier JSON (accents et indentation)."""
    with open(fichier_json, "w", encoding="utf-8") as f:
        json.dump(series, f, ensure_ascii=False, indent=2)


def exporter_csv(series, fichier_csv=FICHIER_CSV):
    """Exporte la collection vers un fichier CSV."""
    with open(fichier_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CHAMPS)
        writer.writeheader()
        for s in series:
            writer.writerow({k: s.get(k, "") for k in CHAMPS})


def importer_csv(fichier_csv=FICHIER_CSV):
    """Importe une collection depuis un fichier CSV en reconvertissant les types."""
    try:
        series = []
        with open(fichier_csv, "r", newline="", encoding="utf-8") as f:
            for ligne in csv.DictReader(f):
                annee_raw = str(ligne.get("annee", "")).strip()
                try:
                    annee = int(annee_raw)
                except ValueError:
                    annee = 0

                note_raw = str(ligne.get("note", "")).strip()
                try:
                    note = float(note_raw)
                except ValueError:
                    note = 0.0

                statut = str(ligne.get("statut", "")).strip() or "À voir"
                titre = str(ligne.get("titre", "")).strip()
                genre = str(ligne.get("genre", "")).strip() or "Non classé"

                if titre:
                    series.append({
                        "titre": titre,
                        "genre": genre,
                        "annee": annee,
                        "note": note,
                        "statut": statut,
                    })
        return series
    except (FileNotFoundError, OSError):
        return []
