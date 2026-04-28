import mysql.connector
from mysql.connector import Error

# On centralise la configuration pour plus de clarté
config = {
    'host': '109.0.170.11',
    'port': 3306,
    'database': 'Jeux',
    'user': 'jeux',
    'password': 'MotDePasse123'
}

def connecter_mariadb():
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"Connecté au serveur MariaDB version {db_info}")
            return connection
    except Error as e:
        print(f"Erreur lors de la connexion : {e}")
        return None

def ajouter_score_snake(nom_joueur, score):
    """Ajoute une ligne à la table Score_SnakePy"""
    connection = connecter_mariadb()
    if connection:
        try:
            cursor = connection.cursor()
            # Requête préparée pour la sécurité
            requete = "INSERT INTO Score_SnakePy (nomJoueur, score) VALUES (%s, %s)"
            valeurs = (nom_joueur, score)
            
            cursor.execute(requete, valeurs)
            connection.commit() # Très important pour valider l'insertion
            print(f"Succès : Score de {nom_joueur} ({score}) enregistré.")
            
        except Error as e:
            print(f"Erreur lors de l'insertion : {e}")
        finally:
            cursor.close()
            connection.close()
            print("Connexion MariaDB fermée.")

if __name__ == "__main__":
    # Test de la nouvelle fonction
    ajouter_score_snake("TestPlayer", 100)