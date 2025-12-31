class Missing(Exception):
    def __init__(self, msg: str):
        self.msg = msg

class Duplicate(Exception):
    def __init__(self, msg: str):
        self.msg = msg 
        
class AuthError(Exception):
    pass

class InvalidToken(AuthError):
    pass

class UserNotFound(AuthError):
    pass