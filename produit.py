"""produit.py — Menu principal de CineTrack (relie api.py et donnees.py)."""

import api
import donnees


def lire_entier(message):
    """Demande un entier à l'utilisateur tant que la saisie est invalide."""
    while True:
        try:
            return int(input(message).strip())
        except ValueError:
            print("  Saisie invalide : veuillez entrer un nombre entier.")


def afficher(series):
    """Affiche toutes les séries enregistrées."""
    if not series:
        print("  (Votre watchlist est vide pour l'instant.)")
        return
    print("\n--- Ma Watchlist ---")
    for i, s in enumerate(series, start=1):
        note_val = s.get("note", 0.0)
        note_txt = f"{note_val:.1f}/10" if isinstance(note_val, (int, float)) and note_val > 0 else "N/A"
        annee_val = s.get("annee", 0)
        annee_txt = annee_val if isinstance(annee_val, int) and annee_val > 0 else "?"
        titre = s.get("titre", "Sans titre")
        genre = s.get("genre", "Non classé")
        statut = s.get("statut", "À voir")
        print(f"  {i}. {titre} ({annee_txt}) | Genre : {genre} | Note : {note_txt} | [{statut}]")


def ajouter_via_api(series):
    """Cherche une série en ligne via l'API, évite les doublons et sauvegarde."""
    titre = input("Titre de la série à rechercher : ").strip()
    if not titre:
        print("  Le titre ne peut pas être vide.")
        return

    for s in series:
        if str(s.get("titre", "")).lower() == titre.lower():
            print(f"  « {s.get('titre')} » est déjà dans votre watchlist !")
            return

    infos = api.chercher_serie(titre)
    if infos:
        for s in series:
            if str(s.get("titre", "")).lower() == infos["titre"].lower():
                print(f"  « {infos['titre']} » est déjà dans votre watchlist !")
                return
        series.append(infos)
        donnees.sauvegarder(series)
        print(f"  Ajouté : {infos['titre']} ({infos['genre']}, {infos['annee']}) — Note {infos['note']:.1f}/10")


def chercher_local(series):
    """Recherche une série dans la liste locale (insensible à la casse)."""
    if not series:
        print("  (Votre watchlist est vide pour l'instant.)")
        return
    mot_cle = input("Nom (ou mot-clé) à chercher : ").strip().lower()
    if not mot_cle:
        print("  Mot-clé vide.")
        return
    resultats = [s for s in series if mot_cle in str(s.get("titre", "")).lower()]
    if resultats:
        afficher(resultats)
    else:
        print("  Aucune série correspondante dans votre watchlist.")


def changer_statut(series):
    """Permet de marquer une série comme 'Vue', 'En cours' ou 'À voir'."""
    afficher(series)
    if not series:
        return
    idx = lire_entier("Numéro de la série à mettre à jour : ")
    if 1 <= idx <= len(series):
        print("  Nouveau statut : 1) À voir   2) En cours   3) Vue")
        choix = input("  Choix : ").strip()
        statuts = {"1": "À voir", "2": "En cours", "3": "Vue"}
        if choix in statuts:
            series[idx - 1]["statut"] = statuts[choix]
            donnees.sauvegarder(series)
            print(f"  Statut mis à jour : {series[idx - 1]['titre']} -> {statuts[choix]}")
        else:
            print("  Choix de statut invalide.")
    else:
        print("  Numéro hors limites.")


def supprimer(series):
    """Supprime une série de la watchlist."""
    afficher(series)
    if not series:
        return
    idx = lire_entier("Numéro de la série à supprimer : ")
    if 1 <= idx <= len(series):
        retiree = series.pop(idx - 1)
        donnees.sauvegarder(series)
        print(f"  « {retiree.get('titre', 'Série')} » supprimée.")
    else:
        print("  Numéro hors limites.")


def statistiques(series):
    """Affiche des statistiques simples sur la watchlist."""
    if not series:
        print("  Aucune donnée pour calculer des statistiques.")
        return
    total = len(series)
    vues = sum(1 for s in series if s.get("statut") == "Vue")
    notes = [s["note"] for s in series if isinstance(s.get("note"), (int, float)) and s["note"] > 0]
    moyenne = sum(notes) / len(notes) if notes else 0.0
    genres = {}
    for s in series:
        g = s.get("genre") or "Non classé"
        genres[g] = genres.get(g, 0) + 1

    print("\n--- Statistiques CineTrack ---")
    print(f"  Total de séries : {total} (dont {vues} vue(s))")
    print(f"  Note moyenne    : {moyenne:.2f}/10")
    print("  Par genre       :", ", ".join(f"{g} ({n})" for g, n in genres.items()))


def menu():
    """Boucle principale du programme."""
    series = donnees.charger()
    while True:
        print("\n=== CineTrack — Gestionnaire de Séries TV ===")
        print("1) Afficher ma watchlist")
        print("2) Ajouter une série (via API TVMaze)")
        print("3) Chercher dans ma liste")
        print("4) Changer le statut (À voir / En cours / Vue)")
        print("5) Supprimer une série")
        print("6) Statistiques")
        print("7) Exporter en CSV")
        print("8) Importer depuis CSV")
        print("9) Quitter")
        choix = input("> ").strip()

        if choix == "1":
            afficher(series)
        elif choix == "2":
            ajouter_via_api(series)
        elif choix == "3":
            chercher_local(series)
        elif choix == "4":
            changer_statut(series)
        elif choix == "5":
            supprimer(series)
        elif choix == "6":
            statistiques(series)
        elif choix == "7":
            donnees.exporter_csv(series)
            print("  Exporté dans series.csv !")
        elif choix == "8":
            imported = donnees.importer_csv()
            if imported:
                series = imported
                donnees.sauvegarder(series)
                print(f"  {len(series)} série(s) importée(s) depuis series.csv !")
            else:
                print("  Aucune donnée valide trouvée dans series.csv.")
        elif choix == "9":
            print("Au revoir !")
            break
        else:
            print("  Choix invalide, réessayez.")


if __name__ == "__main__":
    menu()
