"""produit.py — Menu principal de CineTrack."""

import api
import donnees


def lire_entier(message):
    """Lit un entier de façon sécurisée (ne plante pas sur du texte)."""
    while True:
        try:
            return int(input(message).strip())
        except ValueError:
            print("  Entrez un nombre entier valide.")


def afficher(series):
    """Affiche les séries de la watchlist."""
    if not series:
        print("  (Aucune série enregistrée.)")
        return
    print("\n--- Watchlist ---")
    for i, s in enumerate(series, start=1):
        note_val = s.get("note", 0.0)
        note = f"{note_val:.1f}/10" if isinstance(note_val, (int, float)) and note_val > 0 else "N/A"
        annee_val = s.get("annee", 0)
        annee = annee_val if isinstance(annee_val, int) and annee_val > 0 else "?"
        print(f"  {i}. {s.get('titre', 'Sans titre')} ({annee}) | {s.get('genre', 'Non classé')} | Note: {note} | [{s.get('statut', 'À voir')}]")


def ajouter_serie(series):
    """Ajoute une série via l'API TVMaze en évitant les doublons."""
    titre = input("Titre de la série : ").strip()
    if not titre:
        print("  Titre vide.")
        return

    for s in series:
        if str(s.get("titre", "")).lower() == titre.lower():
            print(f"  « {s['titre']} » est déjà dans la liste.")
            return

    infos = api.chercher_serie(titre)
    if infos is None:
        return

    for s in series:
        if str(s.get("titre", "")).lower() == infos["titre"].lower():
            print(f"  « {infos['titre']} » est déjà dans la liste.")
            return

    series.append(infos)
    donnees.sauvegarder(series)
    print(f"  Ajouté : {infos['titre']} ({infos['genre']}, {infos['annee']})")


def chercher_serie_locale(series):
    """Cherche une série dans la liste locale."""
    if not series:
        print("  (Aucune série enregistrée.)")
        return
    mot = input("Mot-clé : ").strip().lower()
    if not mot:
        print("  Mot-clé vide.")
        return
    trouvees = [s for s in series if mot in str(s.get("titre", "")).lower()]
    if trouvees:
        afficher(trouvees)
    else:
        print("  Aucune série correspondante.")


def changer_statut(series):
    """Change le statut d'une série (À voir / En cours / Vue)."""
    afficher(series)
    if not series:
        return
    idx = lire_entier("Numéro de la série : ")
    if not (1 <= idx <= len(series)):
        print("  Numéro invalide.")
        return

    print("  1) À voir   2) En cours   3) Vue")
    choix = input("  Statut : ").strip()
    statuts = {"1": "À voir", "2": "En cours", "3": "Vue"}
    if choix not in statuts:
        print("  Choix invalide.")
        return

    series[idx - 1]["statut"] = statuts[choix]
    donnees.sauvegarder(series)
    print("  Statut mis à jour.")


def supprimer_serie(series):
    """Supprime une série de la liste."""
    afficher(series)
    if not series:
        return
    idx = lire_entier("Numéro à supprimer : ")
    if not (1 <= idx <= len(series)):
        print("  Numéro invalide.")
        return

    supprimee = series.pop(idx - 1)
    donnees.sauvegarder(series)
    print(f"  « {supprimee.get('titre', 'Série')} » supprimée.")


def afficher_statistiques(series):
    """Affiche des statistiques simples sur la watchlist."""
    if not series:
        print("  Aucune donnée.")
        return
    total = len(series)
    vues = sum(1 for s in series if s.get("statut") == "Vue")
    notes = [s["note"] for s in series if isinstance(s.get("note"), (int, float)) and s["note"] > 0]
    moyenne = sum(notes) / len(notes) if notes else 0.0

    genres = {}
    for s in series:
        g = s.get("genre") or "Non classé"
        genres[g] = genres.get(g, 0) + 1

    print("\n--- Statistiques ---""")
    print(f"  Total : {total} | Vues : {vues} | Note moyenne : {moyenne:.2f}/10")
    print("  Genres :", ", ".join(f"{g} ({n})" for g, n in genres.items()))


def menu():
    """Boucle principale du programme."""
    series = donnees.charger()
    while True:
        print("\n=== CineTrack ===")
        print("1) Afficher")
        print("2) Ajouter (API)")
        print("3) Chercher")
        print("4) Changer statut")
        print("5) Supprimer")
        print("6) Statistiques")
        print("7) Exporter CSV")
        print("8) Importer CSV")
        print("9) Quitter")
        choix = input("> ").strip()

        if choix == "1":
            afficher(series)
        elif choix == "2":
            ajouter_serie(series)
        elif choix == "3":
            chercher_serie_locale(series)
        elif choix == "4":
            changer_statut(series)
        elif choix == "5":
            supprimer_serie(series)
        elif choix == "6":
            afficher_statistiques(series)
        elif choix == "7":
            donnees.exporter_csv(series)
            print("  Exporté vers series.csv.")
        elif choix == "8":
            imported = donnees.importer_csv()
            if imported:
                series = imported
                donnees.sauvegarder(series)
                print(f"  {len(series)} série(s) importée(s).")
            else:
                print("  Aucune donnée dans series.csv.")
        elif choix == "9":
            print("Au revoir !")
            break
        else:
            print("  Choix invalide.")


if __name__ == "__main__":
    menu()
