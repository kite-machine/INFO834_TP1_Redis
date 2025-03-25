import time
import redis
import sys
from collections import Counter

# Configuration Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def log_service_call(email, service_type):
    current_time = int(time.time())
    
    # Clé Redis pour stocker les services utilisés par l'utilisateur
    redis_key = f"user:{email}:services"
    r.rpush(redis_key, f"{current_time}:{service_type}")


def get_recent_users():
    redis_key = "recent_users"
    recent_users = r.lrange(redis_key, 0, -1)
   
    return recent_users

def get_top_users():
    # Récupérer toutes les clés associées aux comptes de connexions des utilisateurs
    users = r.keys('user:*:connections_count')
    user_connections = {}
    
    if not users:
        print("Aucune connexion trouvée pour les utilisateurs.")
    
    for user in users:
        # Récupérer le nombre de connexions de chaque utilisateur
        count = r.get(user)
        if count:  # Si une valeur est trouvée
            # Extraire l'email de la clé
            email = user.split(":")[1]
            user_connections[email] = int(count)
    
    if not user_connections:
        print("Aucun utilisateur n'a de connexions.")
    
    # Trier les utilisateurs par nombre de connexions, par ordre décroissant
    top_users = sorted(user_connections.items(), key=lambda x: x[1], reverse=True)[:3]
    
    # Retourner une liste des utilisateurs triés par nombre de connexions
    return "\n".join([f"{email}:{count}" for email, count in top_users])




def get_least_used_users():
    users = r.keys('user:*:services')
    usage_counts = {}
    for user in users:
        services = r.lrange(user, 0, -1)
        usage_counts[user.split(":")[1]] = len(services)
    least_used = sorted(usage_counts.items(), key=lambda x: x[1])[:3]
    
    return "\n".join([f"{email}:{count}" for email, count in least_used])

def get_most_used_service():
    services = r.keys('user:*:services')
    service_counter = Counter()
    for user in services:
        user_services = r.lrange(user, 0, -1)
        for service in user_services:
            service_type = service.split(":")[1]
            service_counter[service_type] += 1
    most_used_service = service_counter.most_common(1)
    
    return most_used_service[0][0] if most_used_service else None

if __name__ == "__main__":
    if len(sys.argv) == 3:
        email = sys.argv[1]
        service_type = sys.argv[2]
        # Log the service call in Redis
        log_service_call(email, service_type)
        print(f"Service {service_type} logged for {email}")
    elif len(sys.argv) == 2:
        command = sys.argv[1]
        if command == "recent_users":
            print(get_recent_users())
        elif command == "top_users":
            print(get_top_users())
        elif command == "least_used_users":
            print(get_least_used_users())
        elif command == "most_used_service":
            print(get_most_used_service())
