from dataclasses import dataclass, field
import pyotp


@dataclass(slots=True)
class User:
    _id: int = field(default=None)
    _email: str = "e@mail.com"
    _password: str = field(default="")
    _tfa: bool = field(default=False)
    _tfa_key: str = field(init=False, default="")

    def __post_init__(self):
        if self._tfa:
            self._tfa_key = pyotp.random_base32()
        else:
            self._tfa_key = ""

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, to):
        self._id = to

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, to):
        self._email = to

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, to):
        self._password = to

    @property
    def tfa_key(self):
        return self._tfa_key

    @tfa_key.setter
    def tfa_key(self, to):
        self._tfa_key = to

    @property
    def tfa(self):
        return self._tfa

    @tfa.setter
    def tfa(self, to):
        self._tfa = to
