"""api.py — Interrogation de l'API gratuite TVMaze (sans clé API)."""

import requests

BASE_URL = "https://api.tvmaze.com/singlesearch/shows"


def chercher_serie(titre):
    """Recherche une série par son titre sur TVMaze.
    Renvoie un dictionnaire normalisé ou None en cas d'erreur / introuvable.
    """
    titre_propre = str(titre).strip()
    if not titre_propre:
        print("  [Erreur] Le titre de la série est vide.")
        return None

    params = {"q": titre_propre}
    try:
        reponse = requests.get(BASE_URL, params=params, timeout=10)
    except requests.exceptions.RequestException:
        print("  [Erreur réseau] Impossible de contacter le serveur TVMaze.")
        return None

    if reponse.status_code == 404:
        print(f"  [Introuvable] Aucune série trouvée pour « {titre_propre} ».")
        return None
    if reponse.status_code != 200:
        print(f"  [Erreur serveur] Code HTTP {reponse.status_code}.")
        return None

    try:
        data = reponse.json()
    except ValueError:
        print("  [Erreur format] Réponse JSON invalide reçue de l'API.")
        return None

    if not isinstance(data, dict):
        print("  [Erreur format] Données inattendues reçues de l'API.")
        return None

    genres = data.get("genres") or []
    genre_principal = str(genres[0]) if genres else "Non classé"

    premiere = str(data.get("premiered") or "")
    annee_str = premiere[:4]
    annee = int(annee_str) if len(annee_str) == 4 and annee_str.isdigit() else 0

    rating = data.get("rating") or {}
    note = rating.get("average") if isinstance(rating, dict) else None
    try:
        note_val = float(note) if note is not None else 0.0
    except (TypeError, ValueError):
        note_val = 0.0

    nom = str(data.get("name") or titre_propre).strip()

    return {
        "titre": nom,
        "genre": genre_principal,
        "annee": annee,
        "note": note_val,
        "statut": "À voir",
    }
