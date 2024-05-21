import inquirer
from validation import *

login = [
    inquirer.Text('username', message='Enter your username', validate=validateUsername),
    inquirer.Password('password', message='Enter your password')
]

register = [
    inquirer.Text('username', message='Create a username', validate=validateUsername),
    inquirer.Password('password', message='Create a password'),
    inquirer.Text('fname', message='Enter your first name'),
    inquirer.Text('lname', message='Enter your last name'),
]