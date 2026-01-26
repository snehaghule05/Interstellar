import re, hashlib, uuid
from db_config import get_connection

sessions = {}

def validate_email(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(name, email, password,location):
    if not validate_email(email):
        return {"status":"fail","msg":"Invalid Email"}
    if len(password) < 6:
        return {"status":"fail","msg":"Weak Password"}
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users(name,email,password,location) VALUES(%s,%s,%s,%s)",
        (name,email,hash_password(password)))
        conn.commit()
        return {"status":"success"}
    except:
        return {"status":"fail","msg":"Email exists"}
    finally:
        conn.close()
        
def login_user(email, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users WHERE email=%s AND password=%s",
    (email,hash_password(password)))
    user = cur.fetchone()
    conn.close()
    if user:
        token = str(uuid.uuid4())
        sessions[token] = user[0]
        return {"status":"success","token":token}
    return {"status":"fail","msg":"Invalid Credentials"}