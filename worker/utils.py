from secrets import choice
import string

def generate_code(length):
    return ''.join([choice(string.ascii_uppercase + string.digits) for _ in range(length)])