import pymysql
import sys
from config import host, user, password, database

def check_user(email, temp_password):
    try:
        db = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = db.cursor()
        query = "SELECT email FROM utilisateur WHERE email = %s AND mdp = %s"
        cursor.execute(query, (email, temp_password))
        result = cursor.fetchone()

        db.close()

        # Si un résultat est trouvé, l'utilisateur est autorisé
        if result:
            return "authorized"
        else:
            return "unauthorized"

    except pymysql.MySQLError as e:
        print(f"Erreur de connexion : {e}")
        return "error"

if __name__ == "__main__":
    email = sys.argv[1]
    temp_password = sys.argv[2]
    print(check_user(email, temp_password))
