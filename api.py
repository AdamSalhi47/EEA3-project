"""api.py — Recherche d'une série via l'API gratuite TVMaze (sans clé)."""

import requests

URL_API = "https://api.tvmaze.com/singlesearch/shows"


def chercher_serie(titre):
    """Cherche une série sur TVMaze et renvoie un dictionnaire ou None."""
    titre = str(titre).strip()
    if not titre:
        print("  Titre vide.")
        return None

    try:
        reponse = requests.get(URL_API, params={"q": titre}, timeout=10)
    except requests.exceptions.RequestException:
        print("  Erreur réseau : impossible de contacter TVMaze.")
        return None

    if reponse.status_code == 404:
        print(f"  Série introuvable : « {titre} ».")
        return None
    if reponse.status_code != 200:
        print(f"  Erreur serveur (code {reponse.status_code}).")
        return None

    try:
        data = reponse.json()
    except ValueError:
        print("  Réponse JSON invalide.")
        return None

    if not isinstance(data, dict):
        return None

    genres = data.get("genres") or []
    premiere = str(data.get("premiered") or "")
    annee = int(premiere[:4]) if len(premiere) >= 4 and premiere[:4].isdigit() else 0
    note_brute = (data.get("rating") or {}).get("average")
    try:
        note = float(note_brute) if note_brute is not None else 0.0
    except (TypeError, ValueError):
        note = 0.0

    return {
        "titre": str(data.get("name") or titre).strip(),
        "genre": str(genres[0]) if genres else "Non classé",
        "annee": annee,
        "note": note,
        "statut": "À voir",
    }
