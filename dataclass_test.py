from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Person:
    first_name: str
    last_name: str
    age: int
    nickname: Optional[str] = field(default=None)

person = Person("John", "Doe", 30)
print(person.first_name)  # Output: John

### note: you can change any of the values, even replace the types. 
### and you can add new attributes and retrieve them like this
person.foo="bar"
print(person.foo)

# can access like a dict too:
d=person.__dict__
print(d)