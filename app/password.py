from dataclasses import dataclass, field
from password_generator import Password_generator


@dataclass(slots=True)
class Password:
    _name: str = "password name"
    _value: str = field(init=False, default="")
    _user_id: int = field(default=0)
    _length: int = field(default=12)

    def __post_init__(self):
        self._value = Password_generator().generate(self._length, self._user_id)
        # self.password = sha1(self.password.encode()).hexdigest()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, to):
        self._name = to

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, to):
        self._value = to

    @property
    def user_id(self):
        return self._user_id
