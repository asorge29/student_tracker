from inquirer import errors
import pymysql

db = pymysql.connect(host="localhost", user="root", password="1052", database="student_tracker")
crsr = db.cursor()

def validateUsername(answers, username):
    if len(username) <= 3:
        raise errors.ValidationError(username, reason='Username must be at least 4 characters.')
    elif len(username) > 64:
        raise errors.ValidationError(username, reason='Username must be at most 64 characters.')
    return True

def validateNewUsername(answers, username):
    if len(username) <= 3:
        raise errors.ValidationError(username, reason='Username must be at least 4 characters.')
    elif len(username) > 64:
        raise errors.ValidationError(username, reason='Username must be at most 64 characters.')
    elif crsr.execute("SELECT username FROM user_creds where username=%s", (username)):
        raise errors.ValidationError(username, reason='Username already exists.')
    return True

def validatePassword(answers, password):
    if len(password) < 8:
        raise errors.ValidationError(password, reason='Password must be at least 8 characters.')
    elif len(password) > 64:
        raise errors.ValidationError(password, reason='Password must be at most 64 characters.')
    return True

def validateName(answers, name):
    if len(name) < 1:
        raise errors.ValidationError(name, reason='Name must be at least 1 character.')
    elif len(name) > 64:
        raise errors.ValidationError(name, reason='Name must be at most 64 characters.')
    return True