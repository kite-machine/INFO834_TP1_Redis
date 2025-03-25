import redis
import sys
import pymysql
from config import host, user, password

def check_user(email, password):
    db = pymysql.connect(host, user, password, database='tp1')
    cursor = db.cursor()
    
    query = "SELECT email FROM users WHERE email = %s AND password = %s"
    cursor.execute(query, (email, password))
    result = cursor.fetchone()
    
    db.close()
    return result is not None

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "check":
        email = sys.argv[2]
        password = sys.argv[3]
        if check_user(email, password):
            print("authorized")
        else:
            print("unauthorized")