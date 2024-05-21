import inquirer
from validation import *

login = [
    inquirer.Text('username', message='Enter your username', validate=validateUsername),
    inquirer.Password('password', message='Enter your password', validate=validatePassword),
]

register = [
    inquirer.Text('username', message='Create a username', validate=validateNewUsername),
    inquirer.Password('password', message='Create a password', validate=validatePassword),
    inquirer.Text('fname', message='Enter your first name', validate=validateName),
    inquirer.Text('lname', message='Enter your last name', validate=validateName),
]