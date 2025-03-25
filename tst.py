import pymysql

host = 'localhost'
user = 'root'
password = 'password'
database = 'tp1'

try:
    db = pymysql.connect(host=host, user=user, password=password, database=database)
    cursor = db.cursor()
    print("Connexion réussie!")
    query = "SELECT email FROM utilisateur WHERE email = %s AND mdp = %s"
    cursor.execute(query, ('bercier@gmail.com', '1234'))
    result = cursor.fetchone()

    db.close()
    print( result is not None)
except pymysql.MySQLError as e:
    print(f"Erreur de connexion : {e}")
