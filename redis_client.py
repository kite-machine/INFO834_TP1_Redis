import time
import pymysql
import sys
import redis
from config import host, user, password, database

# Configuration Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def check_user(email, temp_password):
    try:
        # Connexion à la base de données MySQL
        db = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = db.cursor()

        # Vérification de l'utilisateur dans la base de données
        query = "SELECT email FROM utilisateur WHERE email = %s AND mdp = %s"
        cursor.execute(query, (email, temp_password))
        result = cursor.fetchone()

        db.close()

        # Si un résultat est trouvé, l'utilisateur est autorisé
        if result:
            # Vérification des connexions dans Redis et ajout des informations récentes
            return check_redis_connections(email)
        else:
            return "unauthorized ,mot de passe incorrect"

    except pymysql.MySQLError as e:
        print(f"Erreur de connexion à MySQL : {e}")
        return "error"

def check_redis_connections(email):
    # Clé Redis pour suivre les connexions de l'utilisateur
    redis_key = f"user:{email}:connections"
    
    # Obtenir le nombre de connexions dans les 10 dernières minutes
    connections = r.lrange(redis_key, 0, -1)
    
    # Supprimer les connexions plus anciennes que 10 minutes
    current_time = int(time.time())
    connections = [timestamp for timestamp in connections if current_time - int(timestamp) < 600]
    
    # Vérifier si l'utilisateur a déjà atteint 10 connexions dans les 10 dernières minutes
    if len(connections) >= 10:
        return "too many connections"
    
    # Ajouter une nouvelle connexion (l'heure actuelle en timestamp Unix)
    r.rpush(redis_key, current_time)
    
    # Limiter la liste à conserver uniquement les connexions dans les 10 dernières minutes
    r.ltrim(redis_key, -10, -1)
    
    redis_key_recent_users = "recent_users"
    r.rpush(redis_key_recent_users, email)
    r.ltrim(redis_key_recent_users, -10, -1)  # Limiter à 10 derniers utilisateurs
    
    redis_key_connections_count = f"user:{email}:connections_count"
    r.incr(redis_key_connections_count)
    
    return "authorized"

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python redis_client.py <email> <password>")
        sys.exit(1)
    
    email = sys.argv[1]
    temp_password = sys.argv[2]
    print(check_user(email, temp_password))
