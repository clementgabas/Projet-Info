import sqlite3
from datetime import datetime

def are_pseudos_friends(pseudo1, pseudo2):
    """
    Fonction qui renvoit True si pseudo1 est ami avec pseudo2, False sinon.

    Parameters
    ----------
    pseudo1 : str
        Pseudo dont on vérifie s'il possède une relation d'amitié avec le pseudo2.
    pseudo2 : str
        Pseudo dont on vérifie si le pseudo1 possède une relation d'amitié avec lui.

    Raises
    ------
    ConnectionAbortedError
        Si une erreur se produit au cours de la connection avec la DB, l'erreur est levée..

    Returns
    -------
    Bool : Bool
        Booléen qui précise si oui ou non le pseudo1 possède une relation d'amitié avec le pseudo 2.

    """
    Bool = False
    try:  # on vérifie si le lien d'amitié n'existe pas déjà
        con = sqlite3.connect("database/apijeux.db")
        cursor = con.cursor()
        cursor.execute("SELECT date_ajout FROM Liste_Amis WHERE pseudo = ? and pseudo_ami = ?", (pseudo1, pseudo2,))
        pse = cursor.fetchone()
    except:
        print("erreur dans are_pseudos_friends")
        raise ConnectionAbortedError
    finally:
        con.close()
    if pse != None: #pseudo1 est ami avec pseudo2
        Bool = True
    else: #pseudo1 n'est pas ami avec pseudo2
        Bool = False
    return Bool

def add_amitie(pseudo1, pseudo2):
    """
    Procédure qui ajoute à pseudo1 une amitié avec pseudo2

    Parameters
    ----------
    pseudo1 : str
        Pseudo pour lequel on ajoute une relation d'amitié avec pseudo2.
    pseudo2 : str
        Pseudo qui va servir à ajouter une relation d'amitié à pseudo1.

    Raises
    ------
    ConnectionAbortedError
        Si une erreur se produit au cours de la communication avec la DB, un rollback jusqu'au commit précédant a lieu et l'erreur est levée.

    Returns
    -------
    None.

    """
    try:  # on ajoute le lien d'amitié
        con = sqlite3.connect("database/apijeux.db")
        cursor = con.cursor()
        date = str(datetime.now())
        cursor.execute("INSERT INTO Liste_Amis (pseudo, pseudo_ami, date_ajout) VALUES (?, ?, ?)", (pseudo1, pseudo2, date,))
        con.commit()
    except:
        print("erreur dans add_amitie")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()

def sup_amitie(pseudo1, pseudo2):
    """
    Procédure qui supprime à pseudo1 son amitié avec pseudo2

    Parameters
    ----------
    pseudo1 : str
        Pseudo pour lequel on va supprimer son lien d'amitié avec pseudo2.
    pseudo2 : str
        Pseudo dont on se sert pour savoir quel lien d'amitié supprimer à pseudo1.

    Raises
    ------
    ConnectionAbortedError
        Si une erreur se produit au cours de la communication avec la DB, un rollback jusqu'au précédant commit à lieu et l'erreur est levée.

    Returns
    -------
    None.

    """
    try:  # on supprime le lien d'amitié
        con = sqlite3.connect("database/apijeux.db")
        cursor = con.cursor()
        cursor.execute("DELETE from Liste_Amis WHERE pseudo = ? and pseudo_ami = ?", (pseudo1, pseudo2))
        con.commit()
    except:
        print("erreur dans sup_amitie")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()

def afficher_liste_amis(pseudo):
    """
    Fonction qui retourne la liste des amis de pseudo

    Parameters
    ----------
    pseudo : str
        Pseudo pour lequel on va afficher la liste de ses amis.

    Raises
    ------
    ConnectionAbortedError
        Si une erreur a lieu au cours de la communication avec la DB, l'erreur est levée.

    Returns
    -------
    liste_amis : list
        Liste des amis de pseudo.

    """
    try: #on affiche la liste des amis
        con = sqlite3.connect("database/apijeux.db")
        cursor= con.cursor()
        cursor.execute("SELECT pseudo_ami, date_ajout FROM Liste_Amis WHERE pseudo = ?", (pseudo,))
        liste_amis = cursor.fetchall()
    except:
        print("ERROR : API.afficherlisteamis :")
        raise ConnectionAbortedError
    finally:
        con.close()
    return liste_amis