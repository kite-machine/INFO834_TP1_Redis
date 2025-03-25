import redis
import sys

def check_user(username):
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    return r.sismember("authorized_users", username)

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "check":
        username = sys.argv[2]
        if check_user(username):
            print("authorized")
        else:
            print("unauthorized")