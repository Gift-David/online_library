
class InvalidEmailError(Exception):
    pass
    # print("Invalid Email")

def validate_email(email):
    if "@" not in email or "." not in email:
        raise InvalidEmailError