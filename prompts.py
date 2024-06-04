import inquirer
from validation import *

login = [
    inquirer.Text('username', message='Enter your username', validate=validateUsername),
    inquirer.Password('password', message='Enter your password', validate=validatePassword),
]

register = [
    inquirer.Text('username', message='Create a username', validate=validateNewUsername),
    inquirer.Password('password', message='Create a password', validate=validateNewPassword),
    inquirer.Text('fname', message='Enter your first name', validate=validateName),
    inquirer.Text('lname', message='Enter your last name', validate=validateName),
]

mainMenu = [
    inquirer.List('mainMenu', message='What do you want to do?', choices=['View Classes & Grades', 'Update Classes & Grades', 'Export Transcript', 'Calculate GPA', 'Update User Info', 'Exit']),
]

updateClasses = [
    inquirer.List('updateClasses', message='What do you want to do?', choices=['Add Class', 'Remove Class', 'Update Class', 'Go Back']),
]

addClass = [
    inquirer.Text('className', message='Enter the name of the class'),
    inquirer.List('grade', message='Select the grade you have in this class', choices=['A', 'B', 'C', 'D', 'F']),
    inquirer.List('current', message='Are you currently taking this class', choices=['Yes', 'No']),
]

updateClass = [
    inquirer.List('updateClass', message='What do you want to do?', choices=['Update Class Name', 'Update Class Grade', 'Update Class Enrollment Status', 'Go Back']),
]