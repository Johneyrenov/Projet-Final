class Livre:
    def __init__(self, isbn, titre, auteur, genre, disponible=True):
        self.isbn = isbn
        self.titre = titre
        self.auteur = auteur
        self.genre = genre
        self.disponible = disponible

    def __str__(self):
        return f"{self.titre} de {self.auteur} ({self.genre}) - ISBN: {self.isbn} - {'Disponible' if self.disponible else 'Emprunte'}"

    def __repr__(self):
        return f"Livre({self.isbn}, {self.titre}, {self.auteur}, {self.genre}, {self.disponible})"


class Utilisateur:
    def __init__(self, user_id, nom, contact):
        self.user_id = user_id
        self.nom = nom
        self.contact = contact
        self.emprunts = []  # Liste des objets Emprunt

    def emprunter(self, emprunt):
        if not isinstance(emprunt, Emprunt):
            raise ValueError(
                "L'objet ajoute doit etre une instance de Emprunt.")
        self.emprunts.append(emprunt)

    def retourner(self, isbn, date_retour):
        for emprunt in self.emprunts:
            if emprunt.isbn == isbn and not emprunt.retourne:
                emprunt.retourne = True
                emprunt.date_retour = date_retour  # Enregistrer la date de retour
                return True  # Retour reussi
        return False  # Aucun emprunt trouve ou deja retourne

    def __str__(self):
        return f"Utilisateur {self.nom} ({self.user_id}) - Contact : {self.contact}"

    def __repr__(self):
        return f"Utilisateur({self.user_id}, {self.nom}, {self.contact})"


class Emprunt:
    def __init__(self, user_id, isbn, date_emprunt, date_retour_prevue, retourne=False, date_retour=None):
        self.user_id = user_id
        self.isbn = isbn
        self.date_emprunt = date_emprunt
        self.date_retour_prevue = date_retour_prevue
        self.retourne = retourne
        self.date_retour = date_retour

    def __str__(self):
        return (f"Emprunt de {self.isbn} par {self.user_id} - Date d'emprunt: {self.date_emprunt} "
                f"- Retour prevu le: {self.date_retour_prevue} - {'Retourner' if self.retourne else 'Non retourner'} "
                f"- Date de retour: {self.date_retour if self.date_retour else 'Non retourner'}")

    def __repr__(self):
        return (f"Emprunt({self.user_id}, {self.isbn}, {self.date_emprunt}, "
                f"{self.date_retour_prevue}, {self.retourne}, {self.date_retour})")
