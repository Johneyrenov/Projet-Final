from fonctions import *
from datetime import datetime
import re


def main():
    FICHIER_LIVRES = "livres.csv"
    FICHIER_UTILISATEURS = "users.csv"
    FICHIER_EMPRUNTS = "emprunts.csv"

    livres = charger_livres(FICHIER_LIVRES)
    utilisateurs = charger_utilisateurs(FICHIER_UTILISATEURS)
    emprunts = charger_emprunts(FICHIER_EMPRUNTS)

    while True:
        afficher_menu()
        choix = ""
        while choix not in ["1", "2", "3", "4", "5"]:
            choix = input("Choisir une option : ")
            if choix not in ["1", "2", "3", "4", "5"]:
                print("Choix incorrect, reessayer ")

        if choix == "1":
            while True:
                effacer()
                sous_menu_livre()
                choix_livre = ""
                while choix_livre not in ["1", "2", "3", "4", "5", "6"]:
                    choix_livre = input("Choisir une option : ")
                    if choix_livre not in ["1", "2", "3", "4", "5", "6"]:
                        print("Choix incorrect, reessayer ")

                if choix_livre == "1":
                    while True:
                        effacer()
                        while True:
                            isbn = input("ISBN du livre : ")
                            if not isbn.strip():
                                print("Erreur : L'ISBN ne peut pas etre vide.")
                            elif not isbn.isdigit():
                                print(
                                    "Erreur : L'ISBN doit contenir uniquement des chiffres(positif).")
                            elif isbn in [livre.isbn for livre in livres]:
                                print(
                                    "Erreur : Cet ISBN existe deja. Veuillez entrer un ISBN unique.")
                            else:
                                break

                        while True:
                            titre = input("Titre du livre : ")
                            if not titre.strip():
                                print("Erreur : Le titre ne peut pas etre vide.")
                            else:
                                break

                        while True:
                            auteur = input("Auteur : ")
                            if not auteur.strip():
                                print("Erreur : L'auteur ne peut pas etre vide.")
                            elif not re.match(r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$', auteur):
                                print(
                                    "Erreur : Le nom de l'auteur ne doit contenir que des lettres.")
                            else:
                                break

                        while True:
                            genre = input("Genre : ")
                            if not genre.strip():
                                print("Erreur : Le genre ne peut pas etre vide.")
                            elif not re.match(r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$', genre):
                                print(
                                    "Erreur : Le genre ne doit contenir que des lettres.")
                            else:
                                break

                        ajouter_livre(FICHIER_LIVRES, livres,
                                      isbn, titre, auteur, genre)
                        print("Livre enregistre avec succes !")

                        Test_confirmation = confirmation_livre()
                        if Test_confirmation == "N":
                            break

                elif choix_livre == "2":
                    while True:
                        effacer()
                        afficher_livres(livres, emprunts)
                        print("\n")
                        while True:
                            isbn = input("ISBN du livre a supprimer : ")
                            if isbn not in [livre.isbn for livre in livres]:
                                print(
                                    "Erreur : Cet ISBN n'existe pas. Veuillez entrer un ISBN valide.\n")
                            else:
                                break

                        livres = supprimer_livre(FICHIER_LIVRES, livres, isbn)
                        print("Livre supprime avec succes !\n")
                        afficher_livres(livres, emprunts)

                        Test_confirmation = confirmation_livre_supprimer()
                        if Test_confirmation == "N":
                            break

                elif choix_livre == "3":
                    while True:
                        effacer()
                        terme = input("Entrez le titre, auteur ou genre : ")
                        while True:
                            resultats = rechercher_livre(
                                livres, terme, emprunts)
                            if resultats:
                                for livre, statut in resultats:
                                    print(
                                        f"ISBN: {livre.isbn} | Titre: {livre.titre} | Auteur: {livre.auteur} | Genre: {livre.genre} | Statut: {statut}")

                                break
                            else:
                                print(
                                    "Erreur : Aucun livre trouve correspondant a votre recherche.")
                                terme = input(
                                    "Entrez un autre titre, auteur ou genre : ")

                        Test_confirmation = confirmation_livre_rechercher()
                        if Test_confirmation == "N":
                            break

                elif choix_livre == "4":
                    effacer()
                    afficher_livres(livres, emprunts)
                    input("Appuyer sur entrer pour retourner...")

                elif choix_livre == "5":
                    while True:
                        effacer()
                        while True:
                            isbn = input("ISBN du livre a mettre a jour : ")
                            if isbn not in [livre.isbn for livre in livres]:
                                print(
                                    "Erreur : Cet ISBN n'existe pas. Veuillez entrer un ISBN valide.")
                            else:
                                break

                        titre = input(
                            "Nouveau titre (laisser vide pour ne pas modifier) : ")
                        auteur = input(
                            "Nouvel auteur (laisser vide pour ne pas modifier) : ")
                        genre = input(
                            "Nouveau genre (laisser vide pour ne pas modifier) : ")
                        mettre_a_jour_livre(
                            FICHIER_LIVRES, livres, isbn, titre, auteur, genre)
                        print("Modification reussie !")
                        Test_confirmation = confirmation_livre_update()
                        if Test_confirmation == "N":
                            break

                elif choix_livre == "6":
                    effacer()
                    break  # Quitte le sous-menu et revient au menu principal

        elif choix == "2":
            while True:
                effacer()
                sous_menu_users()
                choix_utilisateur = ""
                while choix_utilisateur not in ["1", "2", "3", "4"]:
                    choix_utilisateur = input("Choisir une option : ")
                    if choix_utilisateur not in ["1", "2", "3", "4"]:
                        print("Choix incorrect, reessayer ")

                if choix_utilisateur == "1":
                    while True:
                        effacer()

                        while True:
                            user_id = input("ID utilisateur : ")
                            if not user_id.isdigit():
                                print(
                                    "Erreur : L'ID utilisateur doit etre uniquement compose de chiffres.")
                            elif user_id in [utilisateur.user_id for utilisateur in utilisateurs]:
                                print("Erreur : Cet ID utilisateur existe deja.")
                            else:
                                break

                        # Verification du nom de l'utilisateur
                        while True:
                            nom = input("Nom : ")
                            if not nom.isalpha():
                                print(
                                    "Erreur : Le nom doit etre uniquement compose de lettres.")
                            else:
                                break

                        # Verification du contact de l'utilisateur
                        while True:
                            contact = input("Contact : ")
                            if not contact.isdigit():
                                print(
                                    "Erreur : Le contact doit etre uniquement compose de chiffres.")
                            else:
                                break

                        # Ajouter l'utilisateur
                        ajouter_utilisateur(
                            FICHIER_UTILISATEURS, utilisateurs, user_id, nom, contact)
                        print("Utilisateur ajouter avec succes !")
                        Test_confirmation = confirmation_user()
                        if Test_confirmation == "N":
                            break

                elif choix_utilisateur == "2":

                    while True:
                        effacer()

                        # Verification de l'ID utilisateur
                        while True:
                            user_id = input(
                                "ID utilisateur a mettre a jour : ")
                            if user_id not in [utilisateur.user_id for utilisateur in utilisateurs]:
                                print("Erreur : Cet ID utilisateur n'existe pas.")
                            else:
                                break

                          # Demander le nouveau nom et valider
                        while True:
                            nom = input(
                                "Nouveau nom (laisser vide pour ne pas modifier) : ")
                            if nom and not nom.isalpha():
                                print(
                                    "Erreur : Le nom doit etre uniquement compose de lettres.")
                            else:
                                break

                          # Demander le nouveau contact et valider
                        while True:
                            contact = input(
                                "Nouveau contact (laisser vide pour ne pas modifier) :")
                            if contact and not contact.isdigit():  # Validation du contact
                                print(
                                    "Erreur : Le contact doit etre uniquement compose de chiffres.")
                            else:
                                break

                           # Appel de la fonction pour mettre a jour l'utilisateur
                        mettre_a_jour_utilisateur(
                            FICHIER_UTILISATEURS, utilisateurs, user_id, nom if nom else None, contact if contact else None)
                        print("Utilisateur mis a jour avec succes !")

                        # Verifier si l'utilisateur souhaite effectuer une autre mise a jour
                        Test_confirmation = confirmation_user_update()
                        if Test_confirmation == "N":
                            break

                elif choix_utilisateur == "3":
                    while True:
                        effacer()

                        while True:
                            user_id = input("ID utilisateur : ").strip()
                            if user_id not in [utilisateur.user_id for utilisateur in utilisateurs]:
                                print("Erreur : Cet ID utilisateur n'existe pas.")
                            else:
                                break
                        afficher_emprunts_par_utilisateur(emprunts, user_id)
                        input("Appuyez sur Entree pour retourne...")
                        break

                elif choix_utilisateur == "4":
                    effacer()
                    break

        elif choix == "3":
            while True:
                effacer()
                sous_menu_emprunt()
                choix_emprunt = ""
                while choix_emprunt not in ["1", "2", "3"]:
                    choix_emprunt = input("Choisir une option : ")
                    if choix_emprunt not in ["1", "2", "3"]:
                        print("Choix incorrect, reessayer ")

                if choix_emprunt == "1":
                    while True:
                        effacer()

                        while True:
                            user_id = input("ID utilisateur : ")
                            if not user_id.isdigit():
                                print(
                                    "L'ID utilisateur doit etre un nombre. Reessayez.")
                                continue
                            if user_id not in [utilisateur.user_id for utilisateur in utilisateurs]:
                                print("Erreur : Cet ID utilisateur n'existe pas.")
                            else:
                                break
                        while True:
                            isbn = input("ISBN du livre : ")
                            if not isbn.isdigit():
                                print("L'ISBN doit etre un nombre. Reessayez.")
                                continue
                            if isbn not in [livre.isbn for livre in livres]:
                                print(
                                    "Erreur : Cet ISBN n'existe pas. Veuillez entrer un ISBN valide.")
                            else:
                                break

                        while True:
                            date_retour_prevue = input(
                                "Date retour prevue (YYYY-MM-DD) : ")
                            try:

                                date_retour = datetime.strptime(
                                    date_retour_prevue, "%Y-%m-%d")
                            except ValueError:
                                print(
                                    "Erreur : Format de la date incorrect. Veuillez utiliser le format YYYY-MM-DD.")
                                continue

                            # Verification que la date de retour n'est pas dans le passer
                            if date_retour < datetime.now():
                                print(
                                    "Erreur : La date de retour ne peut pas etre anterieure a la date actuelle.")
                                continue
                            else:
                                break
                        enregistrer_emprunt(
                            FICHIER_EMPRUNTS, emprunts, FICHIER_LIVRES, user_id, isbn, date_retour_prevue)
                        print("Emprunt enregistrer")
                        Test_confirmation = confirmation_emprunt()
                        if Test_confirmation == "N":
                            break

                elif choix_emprunt == "2":
                    while True:
                        effacer()
                        while True:
                            # effacer()
                            isbn = input("ISBN du livre retourner : ")
                            if not isbn.isdigit():
                                print("L'ISBN doit etre un nombre. Reessayez.")
                                continue
                            if isbn not in [livre.isbn for livre in livres]:
                                print(
                                    "Erreur : Cet ISBN n'existe pas. Veuillez entrer un ISBN valide.")
                            else:
                                break

                                # Appel de la fonction retourner_livre apres la validation de l'ISBN
                        retourner_livre(FICHIER_EMPRUNTS, emprunts,
                                        FICHIER_LIVRES, livres, isbn)
                        # print("Livre retourne avec succès !")
                        input("Appuyez sur Entree pour retourne...")
                        break

                elif choix_emprunt == "3":
                    effacer()
                    break

        elif choix == "4":
            while True:
                effacer()
                sous_menu_rapport_statistique()

                choix_statistiques = ""
                while choix_statistiques not in ["1", "2", "3", "4"]:
                    choix_statistiques = input("Choisir une option : ")
                    if choix_statistiques not in ["1", "2", "3", "4"]:
                        print("Choix incorrect, réessayer ")

                if choix_statistiques == "1":
                    while True:
                        effacer()
                        # while True:
                        # Appel de la fonction pour generer les statistiques
                        afficher_statut_livres(livres, emprunts)
                        input("\nAppuyez sur Entree pour retourner...")
                        break

                elif choix_statistiques == "2":
                    while True:
                        effacer()
                        # while True:
                        # Appel de la fonction pour generer les statistiques
                        afficher_historique_emprunts_retours(emprunts, livres)
                        input("\nAppuyez sur Entree pour retourner...")
                        break

                elif choix_statistiques == "3":
                    while True:
                        effacer()
                        # while True:
                        # Appel de la fonction pour generer les statistiques
                        afficher_statistiques_genres(emprunts, livres)
                        input("\nAppuyez sur Entree pour retourner...")
                        break

                elif choix_statistiques == "4":
                    effacer()
                    break  # Quitte le sous-menu et retourne au menu principal

        elif choix == "5":
            print("Au revoir !")
            break


if __name__ == "__main__":
    main()
