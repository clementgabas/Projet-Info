import requests
import json
from travailMDP.testmdp import anti_SQl_injection
from RequestsTools.AddressTools import get_absolute_address, make_address

from Player.abstractUser import AbstractUser

absolute_address = get_absolute_address()

class User(AbstractUser):

    def __init__(self, pseudo):
        self.pseudo = pseudo

    def deconnexion(self):
        relative_address = "/home/deconnexion"
        adresse = make_address(absolute_address, relative_address)


        dataPost = {'pseudo': self.pseudo}
        # -- connexion à l'API
        res = requests.get(adresse, data=json.dumps(dataPost))

        if res.status_code == 200:
            Resultat = self.update_resultat(True)
        elif res.status_code == 404:
            Resultat = self.update_resultat(False, "erreur, l'api n'a pas été trouvée")
        elif res.status_code == 500:
            Resultat = self.update_resultat(False, "erreur dans le code de l'api")
        else:
            Resultat = self.update_resultat(False, "erreur non prévue : " + str(res.status_code))
        return Resultat


    def ajout_ami(self,pseudo_ami):
        relative_address = "/home/main/profil/friends"
        adresse = make_address(absolute_address, relative_address)

        if pseudo_ami == self.pseudo:
            Resultat = self.update_resultat(False, "Vous ne pouvez pas vous ajouter vous même comme ami.")
            return Resultat

        dataPost = {'pseudo': self.pseudo, 'pseudo_ami': pseudo_ami}
        # -- connexion à l'API
        res = requests.post(adresse, data=json.dumps(dataPost))
        if res.status_code == 404:
            Resultat = self.update_resultat(False, f"Le pseudo a ajouter à votre liste d'ami ({pseudo_ami}) n'existe pas.")
        elif res.status_code == 208:
            Resultat = self.update_resultat(False, f"Le lien d'amitié avec {pseudo_ami} existe déjà.")
        elif res.status_code == 200:
            Resultat = self.update_resultat(True, f"Votre nouvel ami ({pseudo_ami}) a bien été ajouté à votre liste d'amis.")
        elif res.status_code == 500:
            Resultat = self.update_resultat(False, "erreur dans le code de l'api")
        else:
            Resultat = self.update_resultat(False, "erreur non prévue : " + str(res.status_code))
        return Resultat

    def supp_ami(self,pseudo_ami):
        relative_address = "/home/main/profil/friends"
        adresse = make_address(absolute_address, relative_address)

        if pseudo_ami == self.pseudo:
            Resultat = self.update_resultat(False, "Vous ne pouvez pas vous supprimer vous même comme ami.")
            return Resultat

        dataPost = {'pseudo': self.pseudo, 'pseudo_ami': pseudo_ami}
        # -- connexion à l'API
        res = requests.delete(adresse, data=json.dumps(dataPost))
        if res.status_code == 404:
            Resultat = self.update_resultat(False, f"Le pseudo à supprimer de votre liste d'ami ({pseudo_ami}) n'existe pas.")
        elif res.status_code == 208:
            Resultat = self.update_resultat(False, f"Le lien d'amitié avec {pseudo_ami} n'existe pas.")
        elif res.status_code == 200:
            Resultat = self.update_resultat(True, f"Votre ancien ami ({pseudo_ami}) a bien été supprimé de votre liste d'amis.")
        elif res.status_code == 500:
            Resultat = self.update_resultat(False, "erreur dans le code de l'api")
        else:
            Resultat = self.update_resultat(False, "erreur non prévue : " + str(res.status_code))
        return Resultat

    def afficher_amis(self):
        relative_address = "/home/main/profil/friends"
        adresse = make_address(absolute_address, relative_address)

        dataPost = {'pseudo': self.pseudo}
        # -- connexion à l'API
        res = requests.get(adresse, data=json.dumps(dataPost))

        if res.status_code == 200:
            Resultat = self.update_resultat(True)
            Resultat["Liste_amis"] = res.json()["liste_amis"]
        elif res.status_code == 404:
            Resultat = self.update_resultat(False, "erreur, l'api n'a pas été trouvée")
        elif res.status_code == 500:
            Resultat = self.update_resultat(False, "erreur dans le code de l'api")
        else:
            Resultat = self.update_resultat(False, "erreur non prévue : " + str(res.status_code))
        return Resultat

    def modifier_mdp(self,old_mdp,new_mdp1,new_mdp2):
        relative_address = "/home/main/profil/user/password"
        adresse = make_address(absolute_address, relative_address)

        if new_mdp1 != new_mdp2:
            Resultat = self.update_resultat(False, "Les deux nouveaux mots de passes ne correspondent pas.")
            return Resultat
        if new_mdp1 == "":
            Resultat = self.update_resultat(False, "Veuillez fournir un nouveau mot de passe svp.")
            return Resultat
        if not anti_SQl_injection(new_mdp1):
            Resultat = self.update_resultat(False, "Pour des raisons de sécurité, votre demande ne peut aboutir.")
            return Resultat

        # if not is_mdp_legal(new_mdp1):
        # return self.echec_modif_mdp()

        dataPost = {'pseudo': self.pseudo, 'old_password': old_mdp, 'new_password': new_mdp1}
        res = requests.put(adresse, data=json.dumps(dataPost))

        if res.status_code == 401:
            Resultat = self.update_resultat(False, "Le mot de passe fournit ne correspond pas.")
        elif res.status_code == 200:
            Resultat = self.update_resultat(True, "Le mot de passe a bien été modifié.")
        elif res.status_code == 404:
            Resultat = self.update_resultat(False, "erreur, l'api n'a pas été trouvée")
        elif res.status_code == 500:
            Resultat = self.update_resultat(False, "erreur dans le code de l'api")
        else:
            Resultat = self.update_resultat(False, "erreur non prévue : " + str(res.status_code))
        return Resultat


    def modifier_pseudo(self,new_pseudo):
        relative_address = "/home/main/profil/user/pseudo"
        adresse = make_address(absolute_address, relative_address)

        if new_pseudo == self.pseudo:
            Resultat = self.update_resultat(False, "Le nouveau pseudo est identique à l'ancien.")
            return Resultat

        dataPost = {'old_pseudo': self.pseudo, 'new_pseudo': new_pseudo}
        res = requests.put(adresse, data=json.dumps(dataPost))

        if res.status_code == 409:
            Resultat = self.update_resultat(False, "Le pseudo demandé est déjà utilisé.")
        elif res.status_code == 200:
            self.pseudo = new_pseudo
            Resultat = self.update_resultat(True, "Le pseudo a été mis à jour.")
        elif res.status_code == 404:
            Resultat = self.update_resultat(False, "erreur, l'api n'a pas été trouvée")
        elif res.status_code == 500:
            Resultat = self.update_resultat(False, "erreur dans le code de l'api")
        else:
            Resultat = self.update_resultat(False, "erreur non prévue : " + str(res.status_code))
        return Resultat

    def acceder_stats_perso(self):
        relative_address = "/home/main/profil/user/stat"
        adresse = make_address(absolute_address, relative_address)

        dataPost = {'pseudo': self.pseudo}
        # -- connexion à l'API
        res = requests.get(adresse, data=json.dumps(dataPost))
        if res.status_code == 200:
            stat_perso = res.json()['Statistiques personnelles']
            parties_g = stat_perso[0][1]
            parties_j = stat_perso[0][0]
            pourc_partie_g = 0
            if parties_j != 0:
                pourc_partie_g = parties_g / parties_j * 100
            stat_perso[0].append("{} %".format(pourc_partie_g))
            Resultat = self.update_resultat(True)
            Resultat["stat_perso"] = stat_perso
        elif res.status_code == 404:
            Resultat = self.update_resultat(False, "erreur, l'api n'a pas été trouvée")
        elif res.status_code == 500:
            Resultat = self.update_resultat(False, "erreur dans le code de l'api")
        else:
            Resultat = self.update_resultat(False, "erreur non prévue : " + str(res.status_code))
        return Resultat

    def reinitialiser_stats_perso(self):
        relative_address = "/home/main/profil/user/stat"
        adresse = make_address(absolute_address, relative_address)

        dataPost = {'pseudo': self.pseudo}
        res = requests.put(adresse, data=json.dumps(dataPost))
        if res.status_code == 200:
            Resultat = self.update_resultat(True, "Vos statistiques ont bien été réinitialisées")
        elif res.status_code == 404:
            Resultat = self.update_resultat(False, "erreur, l'api n'a pas été trouvée")
        elif res.status_code == 500:
            Resultat = self.update_resultat(False, "erreur dans le code de l'api")
        else:
            Resultat = self.update_resultat(False, "erreur non prévue : " + str(res.status_code))
        return Resultat

    def aff_classement_general(self):
        relative_address = "/home/main/profil/classment/general"
        adresse = make_address(absolute_address, relative_address)

        # -- connexion à l'API
        dataPost = {"pseudo": self.pseudo}
        res = requests.get(adresse, data=json.dumps(dataPost))

        if res.status_code == 200:
            Resultat = self.update_resultat(True)
            Resultat["classement_general"] = res.json()["classement_general"]
            Resultat["classement_general_amis"] = res.json()["classement_general_amis"]
        elif res.status_code == 404:
            Resultat = self.update_resultat(False, "erreur, l'api n'a pas été trouvée")
        elif res.status_code == 500:
            Resultat = self.update_resultat(False, "erreur dans le code de l'api")
        else:
            Resultat = self.update_resultat(False, "erreur non prévue : " + str(res.status_code))
        return Resultat

    def aff_classement_jeu_oie(self):
        relative_address = "/home/main/profil/classment/jeu"
        adresse = make_address(absolute_address, relative_address)

        # -- connexion à l'API
        dataPost = {"nom_jeu": "Oie", "pseudo": self.pseudo}
        res = requests.get(adresse, data=json.dumps(dataPost))

        if res.status_code == 200:
            Resultat = self.update_resultat(True)
            Resultat["classement_jeu"] = res.json()["classement_jeu"]
            Resultat["classement_jeu_amis"] = res.json()["classement_jeu_amis"]
        elif res.status_code == 404:
            Resultat = self.update_resultat(False, "erreur, l'api n'a pas été trouvée")
        elif res.status_code == 500:
            Resultat = self.update_resultat(False, "erreur dans le code de l'api")
        else:
            Resultat = self.update_resultat(False, "erreur non prévue : " + str(res.status_code))
        return Resultat

    def aff_classement_P4(self):
        relative_address = "/home/main/profil/classment/jeu"
        adresse = make_address(absolute_address, relative_address)

        # -- connexion à l'API
        dataPost = {"nom_jeu": "P4", "pseudo": self.pseudo}
        res = requests.get(adresse, data=json.dumps(dataPost))

        if res.status_code == 200:
            Resultat = self.update_resultat(True)
            Resultat["classement_jeu"] = res.json()["classement_jeu"]
            Resultat["classement_jeu_amis"] = res.json()["classement_jeu_amis"]
        elif res.status_code == 404:
            Resultat = self.update_resultat(False, "erreur, l'api n'a pas été trouvée")
        elif res.status_code == 500:
            Resultat = self.update_resultat(False, "erreur dans le code de l'api")
        else:
            Resultat = self.update_resultat(False, "erreur non prévue : " + str(res.status_code))
        return Resultat