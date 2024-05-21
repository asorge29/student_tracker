import re
import inquirer
import pymysql
from rich import print
from prompts import *

db = pymysql.connect(host="localhost", user="root", password="1052", database="student_tracker")
db.autocommit(True)
crsr = db.cursor()

intent = inquirer.list_input("What do you want to do?", choices=["Log In", "Register", "Exit"])

if intent == "Log In":
    creds = inquirer.prompt(login)
elif intent == "Register":
    info = inquirer.prompt(register)
    crsr.execute("INSERT INTO user_creds (username, password) VALUES (%s, %s)", (info["username"], info["password"]))
    id = crsr.lastrowid
    crsr.execute("INSERT INTO user_info (id, fname, lname) VALUES (%s, %s, %s)", (id, info["fname"], info["lname"]))
else:
    exit()