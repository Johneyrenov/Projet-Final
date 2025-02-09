import csv
import os
from datetime import datetime
from classes import Livre, Utilisateur, Emprunt
from collections import Counter


# livres


def charger_livres(fichier_livres):
    livres = []
    try:
        with open(fichier_livres, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                livres.append(Livre(
                    row["isbn"],
                    row["titre"],
                    row["auteur"],
                    row["genre"],
                    row["disponible"].lower() == "true"  # Convertir en booleen
                ))
    except FileNotFoundError:
        print("Fichier livres.csv non trouve.")
    return livres


def sauvegarder_livres(fichier_livres, livres):
    with open(fichier_livres, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["isbn", "titre", "auteur",
                        "genre", "disponible"])  # En-tete
        for livre in livres:
            writer.writerow([
                livre.isbn,
                livre.titre,
                livre.auteur,
                livre.genre,
                "True" if livre.disponible else "False"
            ])


def retourner_livre(fichier_emprunts, emprunts, fichier_livres, livres, isbn):
    # Verifier si le livre a ete emprunte et non encore retourne
    livre_trouve = False
    for emprunt in emprunts:
        if emprunt.isbn == isbn:
            livre_trouve = True
            if emprunt.retourne:
                print(
                    f"Erreur : Le livre avec ISBN {isbn} a deja ete retourne.")
                return
            else:
                emprunt.retourne = True
                emprunt.date_retour = datetime.now().strftime('%Y-%m-%d')
                break

    if not livre_trouve:
        print(
            f"Erreur : Le livre avec ISBN {isbn} n'a pas ete emprunte et ne peut pas etre retourne.")
        return

    # Mettre a jour l'etat du livre pour le rendre disponible
    for livre in livres:
        if livre.isbn == isbn:
            livre.disponible = True
            break

    # Sauvegarde des emprunts et des livres apres modification
    sauvegarder_emprunts(fichier_emprunts, emprunts)
    sauvegarder_livres(fichier_livres, livres)

    print(f"Livre avec ISBN {isbn} retourne avec succes.")


def ajouter_livre(fichier_csv, livres, isbn, titre, auteur, genre):
    # Normalisation du genre en majuscules
    genre_normalise = genre.strip().upper()
    titre_normalise = titre.strip().upper()
    auteur_normalise = auteur.strip().upper()

    nouveau_livre = Livre(isbn, titre_normalise, auteur_normalise,
                          genre_normalise, disponible=True)  # Disponible par défaut
    livres.append(nouveau_livre)
    sauvegarder_livres(fichier_csv, livres)


def mettre_a_jour_livre(fichier_csv, livres, isbn, titre=None, auteur=None, genre=None):
    livre_trouve = False
    for livre in livres:
        if livre.isbn == isbn:
            if titre:
                livre.titre = titre.strip().upper()
            if auteur:
                livre.auteur = auteur.strip().upper()
            if genre:
                livre.genre = genre.strip().upper()
            livre_trouve = True
            # Une fois le livre trouve et mis a jour, on peut sortir de la boucle.
            break

    if livre_trouve:
        sauvegarder_livres(fichier_csv, livres)
        print(f"Le livre avec ISBN {isbn} a ete mis a jour.")
    else:
        print(f"Aucun livre trouve avec ISBN {isbn}.")


def supprimer_livre(fichier_csv, livres, isbn):
    livres = [livre for livre in livres if livre.isbn != isbn]
    sauvegarder_livres(fichier_csv, livres)
    return livres


def rechercher_livre(livres, terme, emprunts):
    resultats = []
    for livre in livres:
        # Verification si le livre correspond au terme de recherche (titre, auteur ou genre)
        if (terme.lower() in livre.titre.lower() or
            terme.lower() in livre.auteur.lower() or
                terme.lower() in livre.genre.lower()):

            # Verifier si le livre est emprunte
            emprunte = any(emprunt.isbn == livre.isbn for emprunt in emprunts)

            # Ajouter le livre aux resultats avec son statut
            statut = "Non disponible" if emprunte else "Disponible"
            resultats.append((livre, statut))

    return resultats


def afficher_livres(livres, emprunts):
    for livre in livres:
        emprunte = any(emprunt.isbn == livre.isbn for emprunt in emprunts)

        statut = "Non disponible" if emprunte else "Disponible"

        if statut == "Non disponible" and any(emprunt.isbn == livre.isbn and emprunt.retourne for emprunt in emprunts):
            statut = "Disponible"

        print(
            f"ISBN: {livre.isbn} | Titre: {livre.titre} | Auteur: {livre.auteur} | Genre: {livre.genre} | Statut: {statut}")


# users

def charger_utilisateurs(fichier_csv):
    utilisateurs = []
    try:
        with open(fichier_csv, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            # Convertir en liste pour eviter de consommer l'iterateur
            lignes = list(reader)

            if not lignes:  # Verifier si la liste est vide
                print(f"{fichier_csv} est vide.")
                return utilisateurs  # Retourne une liste vide si le fichier est vide

            for row in lignes:
                utilisateur = Utilisateur(
                    row['user_id'], row['nom'], row['contact'])
                utilisateurs.append(utilisateur)
    except FileNotFoundError:
        print(f"Le fichier {fichier_csv} est introuvable.")
    return utilisateurs


def sauvegarder_utilisateurs(fichier_csv, utilisateurs):
    with open(fichier_csv, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['user_id', 'nom', 'contact']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for utilisateur in utilisateurs:
            writer.writerow({'user_id': utilisateur.user_id,
                            'nom': utilisateur.nom, 'contact': utilisateur.contact})


def ajouter_utilisateur(fichier_csv, utilisateurs, user_id, nom, contact):
    utilisateur = Utilisateur(user_id, nom, contact)
    utilisateurs.append(utilisateur)
    sauvegarder_utilisateurs(fichier_csv, utilisateurs)


def mettre_a_jour_utilisateur(fichier_csv, utilisateurs, user_id, nom=None, contact=None):
    utilisateur_trouve = False
    for utilisateur in utilisateurs:
        if utilisateur.user_id == user_id:
            if nom:
                utilisateur.nom = nom
            if contact:
                utilisateur.contact = contact
            utilisateur_trouve = True
            break  # On sort des qu'on a trouve et mis a jour l'utilisateur.

    if utilisateur_trouve:
        sauvegarder_utilisateurs(fichier_csv, utilisateurs)
        print(f"L'utilisateur avec ID {user_id} a ete mis à jour.")
    else:
        print(f"Aucun utilisateur trouve avec ID {user_id}.")
        
def afficher_utilisateurs(utilisateurs):
    if not utilisateurs:
        print("Aucun utilisateur enregistré.")
    else:
        print("\n=== Liste des Utilisateurs ===")
        for utilisateur in utilisateurs:
            print(utilisateur)
# emprunts

def charger_emprunts(fichier_emprunts):
    emprunts = []
    try:
        with open(fichier_emprunts, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            lignes = list(reader)

            # Si le fichier est vide ou ne contient que l'en-tete
            if not lignes or len(lignes) == 1:
                print("Erreur : Le fichier est vide.")
                return emprunts

            lignes = iter(lignes)
            next(lignes)
            for row in lignes:
                if len(row) == 6:
                    user_id, isbn, date_emprunt, date_retour_prevue, retourne, date_retour = row
                    emprunt = Emprunt(
                        user_id, isbn, date_emprunt, date_retour_prevue, retourne == 'True', date_retour)
                    emprunts.append(emprunt)
                else:
                    print(
                        f"Avertissement : ligne ignore car elle n'a pas 6 valeurs : {row}")
    except FileNotFoundError:
        print(f"Le fichier {fichier_emprunts} est introuvable.")
    return emprunts


def enregistrer_emprunt(fichier_emprunts, emprunts, fichier_livres, user_id, isbn, date_retour_prevue):
    livres = charger_livres(fichier_livres)  # Charger tous les livres

    nouvel_emprunt = Emprunt(user_id, isbn, datetime.now().strftime(
        '%Y-%m-%d'), date_retour_prevue, False)
    emprunts.append(nouvel_emprunt)
    sauvegarder_emprunts(fichier_emprunts, emprunts)

    # Mise a jour de la disponibilite du livre emprunte
    for livre in livres:
        if livre.isbn == isbn:
            livre.disponible = False  # Rendre le livre indisponible
            break

    # Sauvegarder tous les livres mis a jour
    sauvegarder_livres(fichier_livres, livres)


def sauvegarder_emprunts(FICHIER_EMPRUNTS, emprunts):
    with open(FICHIER_EMPRUNTS, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["user_id", "isbn", "date_emprunt",
                        "date_retour_prevue", "retourne", "date_retour"])

        for emprunt in emprunts:
            writer.writerow([emprunt.user_id, emprunt.isbn, emprunt.date_emprunt,
                            emprunt.date_retour_prevue, emprunt.retourne, emprunt.date_retour])


def afficher_emprunts_par_utilisateur(emprunts, user_id):
    emprunts_utilisateur = [
        e for e in emprunts if e.user_id == user_id and not e.retourne]

    if not emprunts_utilisateur:
        print(f"Aucun emprunt en cours trouve pour l'utilisateur {user_id}.")
        return

    print(f"\n===== Emprunts en cours pour l'utilisateur {user_id} =====\n")
    for emprunt in emprunts_utilisateur:
        print(
            f"ISBN: {emprunt.isbn} | Date d'emprunt: {emprunt.date_emprunt} | Retour prevu: {emprunt.date_retour_prevue}")


# statistiques

def afficher_statut_livres(livres, emprunts):
    print("\n===== STATUT DES LIVRES =====\n")

    livres_empruntes = {
        emprunt.isbn for emprunt in emprunts if not emprunt.retourne}

    print("Livres disponibles :")
    for livre in livres:
        if livre.isbn not in livres_empruntes:
            print(f"{livre.titre} ({livre.auteur}) - Genre : {livre.genre}")

    print("\nLivres empruntes :")
    for livre in livres:
        if livre.isbn in livres_empruntes:
            print(f"{livre.titre} ({livre.auteur}) - Genre : {livre.genre}")


def afficher_historique_emprunts_retours(emprunts, livres):
    print("\n===== HISTORIQUE DES EMPRUNTS ET RETOURS =====\n")

    if not emprunts:
        print("Aucun emprunt enregistre.")
        return

    for emprunt in emprunts:
        # Trouver le livre correspondant a cet emprunt
        livre = next(
            (livre for livre in livres if livre.isbn == emprunt.isbn), None)

        if livre:
            statut_retour = "Retourner" if emprunt.retourne else "Non retourner"
            print(
                f"ISBN: {livre.isbn} | Titre: {livre.titre} | Auteur: {livre.auteur} | Genre: {livre.genre}")
            print(
                f"Date d'emprunt: {emprunt.date_emprunt} | Date de retour prevue: {emprunt.date_retour_prevue}")
            if emprunt.retourne:
                print(f"Date de retour: {emprunt.date_retour}")
            print(f"Statut: {statut_retour}\n")
        else:
            print(f"Erreur: Livre avec ISBN {emprunt.isbn} non trouve.")


def afficher_statistiques_genres(emprunts, livres):
    # Creer un dictionnaire pour associer chaque ISBN a son genre
    isbn_to_genre = {livre.isbn: livre.genre for livre in livres}

    # Liste des genres empruntes
    genres_empruntes = []

    for emprunt in emprunts:
        genre = isbn_to_genre.get(emprunt.isbn)
        if genre:
            genres_empruntes.append(genre)

    # Compter le nombre d'emprunts par genre
    compteur_genres = Counter(genres_empruntes)

    if not compteur_genres:
        print("Aucun emprunt enregistre.")
        return

    # Afficher les genres les plus empruntes
    print("\n===== STATISTIQUES DES GENRES LES PLUS EMPRUNTES =====\n")
    for genre, count in compteur_genres.most_common():
        print(f"Genre: {genre} - Nombre d'emprunts: {count}")


def confirmation_livre():
    while True:
        choix = input(
            "Voulez-vous enregistre un autre livre ? (O/N) : ").strip().upper()
        if choix in ["O", "N"]:
            return choix
        print("Erreur, saisir O pour oui ou N pour non")


def confirmation_livre_supprimer():
    while True:
        choix = input(
            "Voulez-vous supprimer un autre livre ? (O/N) : ").strip().upper()
        if choix in ["O", "N"]:
            return choix
        print("Erreur, saisir O pour oui ou N pour non")


def confirmation_livre_rechercher():
    while True:
        choix = input(
            "Voulez-vous rechercher un autre livre ? (O/N) : ").strip().upper()
        if choix in ["O", "N"]:
            return choix
        print("Erreur, saisir O pour oui ou N pour non")


def confirmation_livre_update():
    while True:
        choix = input(
            "Voulez-vous modifier un autre livre ? (O/N) : ").strip().upper()
        if choix in ["O", "N"]:
            return choix
        print("Erreur, saisir O pour oui ou N pour non")


def confirmation_user():
    while True:
        choix = input(
            "Voulez-vous ajouter un autre utilisateur ? (O/N) : ").strip().upper()
        if choix in ["O", "N"]:
            return choix
        print("Erreur, saisir O pour oui ou N pour non")


def confirmation_user_update():
    while True:
        choix = input(
            "Voulez-vous modifier un autre utilisateur ? (O/N) : ").strip().upper()
        if choix in ["O", "N"]:
            return choix
        print("Erreur, saisir O pour oui ou N pour non")


def confirmation_emprunt():
    while True:
        choix = input(
            "Voulez-vous enregistrer un autre emprunt ? (O/N) : ").strip().upper()
        if choix in ["O", "N"]:
            return choix
        print("Erreur, saisir O pour oui ou N pour non")


def afficher_menu():
    print("\n===== MENU BIBLIOTHEQUE =====\n")
    print("1. Presser [1] pour mener les operations sur les livres.")
    print("2. Presser [2] pour mener les operations sur les utilisateurs.")
    print("3. Presser [3] pour la gestion des emprunts et retour.")
    print("4. Presser [4] pour le rapport et statistique.")
    print("5. Presser [5] pour quitter.")


def sous_menu_livre():

    print("\n===== GESTION DES LIVRES =====\n")
    print("1. Presser [1] pour ajouter un livre.")
    print("2. Presser [2] pour supprimer un livre.")
    print("3. Presser [3] pour rechercher un livre.")
    print("4. Presser [4] pour afficher tous les livres.")
    print("5. Presser [5] pour mettre a jour un livre.")
    print("6. Presser [6] pour retourner au menu principal.")


def sous_menu_users():

    print("\n===== GESTION DES UTILISATEURS =====\n")
    print("1. Presser [1] pour ajouter un utilisateur.")
    print("2. Presser [2] pour mettre a jour un utilisateur.")
    print("3. Presser [3] pour voir les emprunts d'un utilisateur.")
    print("4. Presser [4] pour afficher la liste des utilisateurs")
    print("4. Presser [5] pour retourner au menu principal.")


def sous_menu_emprunt():
    print("\n===== GESTION DES EMPRUNTS ET RETOUR =====\n")
    print("1. Presser [1] pour enregistrer un emprunt.")
    print("2. Presser [2] pour retourner un livre.")
    print("3. Presser [3] pour retourner au menu principal.")


def sous_menu_rapport_statistique():
    print("\n===== RAPPORT ET STATISTIQUE =====\n")
    print(
        "1. Presser [1] pour voir les livres actuellement disponible et emprunte.")
    print("2. Presser [2] pour l'historique des emprunts et retour.")
    print(
        "3. Presser [3] pour la statistiques sur les genres les plus empruntes.")
    print("4. Presser [4] pour retourner au menu principal.")


def effacer():
    os.system('cls' if os.name == 'nt' else 'clear')
