from string import ascii_uppercase, digits
from random import choice
from datetime import datetime


def generate_id(prefix="", length=30):
    letters = ascii_uppercase + digits
    return prefix.__add__( "".join([ choice(letters) for _ in range(length) ]) )


def get_current_epoch():
    return datetime.now().timestamp()