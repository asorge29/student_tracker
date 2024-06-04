import inquirer
import pymysql
from rich import print
from prompts import *
from validation import *
from tkinter.filedialog import asksaveasfilename
from os import system, path

db = pymysql.connect(host="localhost", user="root", password="399764abc", database="student_tracker")
db.autocommit(True)
crsr = db.cursor()

def saveTranscript(transcript):
    file = asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file:
        with open(file, "w") as f:
            f.write(transcript)

def cls():
    if system == "Windows":
        system("cls")
    else:
        system("clear")

intent = inquirer.list_input("What do you want to do? (Select with arrow keys)", choices=["Log In", "Register", "Exit"])
cls()

if intent == "Log In":
    creds = inquirer.prompt(login)
    username, password = creds["username"], creds["password"]
    crsr.execute("select fname, lname, id from user_info where id=(select id from user_creds where username=%s)", (creds["username"]))
    fname, lname, userID = crsr.fetchone()
    cls()
    choice = {"mainMenu":str}
    while choice['mainMenu'] != "Exit":
        cls()
        print(f"[green]Welcome back, {fname}!")
        choice = inquirer.prompt(mainMenu)
        cls()
        if choice['mainMenu'] == "View Classes & Grades":
            crsr.execute("select name, grade from classes where student_id=%s", (userID))
            classes = crsr.fetchall()
            print(f"[green]{fname}'s Classes & Grades:[/green]")
            for i in classes:
                print(f"Class: {i[0]} | Grade: {i[1]}")
            input("Press enter to continue...")
            cls()
        elif choice['mainMenu'] == "Update Classes & Grades":
            updateChoice = inquirer.prompt(updateClasses)
            cls()
            while updateChoice['updateClasses']!= "Go Back":
                if updateChoice['updateClasses'] == "Add Class":
                    newClass = inquirer.prompt(addClass)
                    cls()
                    if newClass['current'] == "Yes":
                        newClass['current'] = 1
                    else:
                        newClass['current'] = 0
                    print("[yellow]Adding Class...")
                    crsr.execute("insert into classes (student_id, name, grade, current) values (%s, %s, %s, %s)", (userID, newClass['className'], newClass['grade'], newClass['current']))
                    print("[green]Class Added!")
                    input("Press Enter to continue...")
                    cls()
                elif updateChoice['updateClasses'] == "Remove Class":
                    crsr.execute("select name, id from classes where student_id=%s", (userID))
                    classes = crsr.fetchall()
                    toRemove = inquirer.list_input("Select the class you want to remove", choices=[i[0] for i in classes])
                    cls()
                    toRemoveId = [i[1] for i in classes if i[0] == toRemove][0]
                    print("[yellow]Removing Class...")
                    crsr.execute("delete from classes where id=%s", (toRemoveId))
                    print("[green]Class Removed!")
                    input("Press Enter to continue...")
                    cls()
                elif updateChoice['updateClasses'] == "Update Class":
                    updateType = inquirer.prompt(updateClass)
                    cls()
                    while updateType['updateClass']!= "Go Back":
                        crsr.execute("select name, id from classes where student_id=%s", (userID))
                        classes = crsr.fetchall()
                        toUpdate = inquirer.list_input("Select the class you want to update", choices=[i[0] for i in classes])
                        cls()
                        toUpdateId = [i[1] for i in classes if i[0] == toUpdate][0]   
                        if updateType['updateClass'] == "Update Class Name":
                            newName = inquirer.text("Enter the new class name")
                            print("[yellow]Updating Class Name...")
                            crsr.execute("update classes set name=%s where id=%s", (newName, toUpdateId))
                            print("[green]Class Name Updated!")
                            input("Press Enter to continue...")
                            cls()
                        elif updateType['updateClass'] == "Update Class Grade":
                            newGrade = inquirer.list_input("Select the new grade", choices=['A', 'B', 'C', 'D', 'F'])
                            print("[yellow]Updating Class Grade...")
                            crsr.execute("update classes set grade=%s where id=%s", (newGrade, toUpdateId))
                            print("[green]Class Grade Updated!")
                            input("Press Enter to continue...")
                            cls()
                        elif updateType['updateClass'] == "Update Class Enrollment Status":
                            newStatus = inquirer.list_input("Select the new enrollment status", choices=['Yes', 'No'])
                            if newStatus == "Yes":
                                newStatus = 1
                            else:
                                newStatus = 0
                            print("[yellow]Updating Class Enrollment Status...")
                            crsr.execute("update classes set current=%s where id=%s", (newStatus, toUpdateId))
                            print("[green]Class Enrollment Status Updated")
                            input("Press Enter to continue...")
                            cls()
                        updateType = inquirer.prompt(updateClass)
                        cls()
                updateChoice = inquirer.prompt(updateClasses)
                cls()
        elif choice['mainMenu'] == "Export Transcript":
            print("[yellow]Exporting Transcript...")
            with open(path.expanduser("~/Desktop/transcript.txt"), "w") as f:
                f.write(f"Transcript for {fname} {lname}\n")
                f.write("----------------------------------------\n")
                crsr.execute("select name, grade from classes where student_id=%s and current=1", (userID))
                currentClasses = crsr.fetchall()
                f.write("Current Classes:\n")
                for i in currentClasses:
                    f.write(f"{i[0]}: {i[1]}\n")
                f.write("----------------------------------------\n")
                crsr.execute("select name, grade from classes where student_id=%s and current=0", (userID))
                pastClasses = crsr.fetchall()
                f.write("Past Classes:\n")
                for i in pastClasses:
                    f.write(f"{i[0]}: {i[1]}\n")
                f.write("----------------------------------------\n")
                crsr.execute("select grade from classes where student_id=%s", (userID))
                grades = crsr.fetchall()
                grades = [i[0] for i in grades]
                for i in range(len(grades)):
                    if grades[i] == "A":
                        grades[i] = 4.0
                    elif grades[i] == "B":
                        grades[i] = 3.0
                    elif grades[i] == "C":
                        grades[i] = 2.0
                    elif grades[i] == "D":
                        grades[i] = 1.0
                    elif grades[i] == "F":
                        grades[i] = 0.0
                points = 0
                for i in grades:
                    points += i
                gpa = points / len(grades)
                gpa = round(gpa, 2)
                f.write(f"GPA: {gpa}")
                f.write("\n----------------------------------------\n")
                f.write(f"End of Transcript")
                f.close()
            print("[green]Transcript Exported!")
            input("Press Enter to continue...")
            cls()
        elif choice['mainMenu'] == "Calculate GPA":
            crsr.execute("select grade from classes where student_id=%s", (userID))
            grades = crsr.fetchall()
            grades = [i[0] for i in grades]
            for i in range(len(grades)):
                if grades[i] == "A":
                    grades[i] = 4.0
                elif grades[i] == "B":
                    grades[i] = 3.0
                elif grades[i] == "C":
                    grades[i] = 2.0
                elif grades[i] == "D":
                    grades[i] = 1.0
                elif grades[i] == "F":
                    grades[i] = 0.0
            points = 0
            for i in grades:
                points += i
            gpa = points / len(grades)
            gpa = round(gpa, 2)
            print(f"Your GPA is: {gpa}")
            input("Press Enter to continue...")
            cls()
        elif choice['mainMenu'] == "Update User Info":
            infoChoice = inquirer.prompt(updateInfo)
            cls()
            while infoChoice['updateInfo']!= "Go Back":
                if infoChoice['updateInfo'] == "Update First Name":
                    print(f"Your current first name is: {fname}")
                    newFname = inquirer.text("Enter your new first name", validate=validateName)
                    cls()
                    crsr.execute("update user_creds set first_name=%s where id=%s", (newFname, userID))
                    print("[green]First Name Updated!")
                elif infoChoice['updateInfo'] == "Update Last Name":
                    print(f"Your current last name is: {lname}")
                    newLname = inquirer.text("Enter your new last name", validate=validateName)
                    cls()
                    crsr.execute("update user_creds set last_name=%s where id=%s", (newLname, userID))
                    print("[green]Last Name Updated!")
                elif infoChoice['updateInfo'] == "Update Username":
                    print(f"Your current username is: {username}")
                    newUsername = inquirer.text("Enter your new username", validate=validateNewUsername)
                    cls()
                    crsr.execute("update user_creds set username=%s where id=%s", (newUsername, userID))
                    print("[green]Username Updated!")
                elif infoChoice['updateInfo'] == "Update Password":
                    print(f"Your current password is: {password}")
                    newPassword = inquirer.password("Enter your new password", validate=validateNewPassword)
                    cls()
                    crsr.execute("update user_creds set password=%s where id=%s", (newPassword, userID))
                    print("[green]Password Updated!")
                infoChoice = inquirer.prompt(updateInfo)
                cls()
    cls()
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