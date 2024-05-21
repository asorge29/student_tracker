from inquirer import errors

def validateUsername(answers, username):
    if len(username) < 3:
        raise errors.ValidationError('Username must be at least 3 characters.')
    elif len(username) > 64:
        raise errors.ValidationError('Username must be at most 64 characters.')
    return True