class UserAlreadyExist(Exception):
    def __init__(self, username, message="User already registered"):
        self.username = username
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.username} -> {self.message}'

class UserNotFound(Exception):
    def __init__(self, username, message="User not found"):
        self.username = username
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.username} -> {self.message}'

class WrongPassword(Exception):
    def __init__(self, message="Wrong password"):
        self.message = message
        super().__init__(self.message)

class WrongKey(Exception):
    def __init__(self, message="Wrong decryption key"):
        self.message = message
        super().__init__(self.message)

class RoomNotFound(Exception):
    def __init__(self, room, message="Room not found"):
        self.room = room
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return  f'{self.room} -> {self.message}'

class SettingNotFound(Exception):
    def __init__(self, setting, message="Setting does not exist"):
        self.setting = setting
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.setting} -> {self.message}'