import inquirer
import pymysql
from rich import print
from prompts import *
from tkinter.filedialog import asksaveasfilename
from os import system

db = pymysql.connect(host="localhost", user="root", password="399764abc", database="student_tracker")
db.autocommit(True)
crsr = db.cursor()

def saveTranscript(transcript):
    file = asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file:
        with open(file, "w") as f:
            f.write(transcript)

def clearTerm():
    if system == "Windows":
        system("cls")
    else:
        system("clear")

intent = inquirer.list_input("What do you want to do? (Select with arrow keys)", choices=["Log In", "Register", "Exit"])
clearTerm()

if intent == "Log In":
    creds = inquirer.prompt(login)
    crsr.execute("select fname, lname from user_info where id=(select id from user_creds where username=%s)", (creds["username"]))
    fname, lname = crsr.fetchone()
    clearTerm()
    choice = {"mainMenu":str}
    while choice['mainMenu'] != "Exit":
        clearTerm()
        print(f"[green]Welcome back, {fname}!")
        choice = inquirer.prompt(mainMenu)
        print(f"[green]Your choice:[/green] [red][underline]{choice['mainMenu']}")
    clearTerm()
    print("[red]Exiting...")
    print("[green]Goodbye!")
    exit()
elif intent == "Register":
    info = inquirer.prompt(register)
    if info:
        crsr.execute("INSERT INTO user_creds (username, password) VALUES (%s, %s)", (info["username"], info["password"]))
        id = crsr.lastrowid
        crsr.execute("INSERT INTO user_info (id, fname, lname) VALUES (%s, %s, %s)", (id, info["fname"], info["lname"]))
else:
    exit()