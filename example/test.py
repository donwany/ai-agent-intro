from pydantic import BaseModel


# python dataclass

class Person(BaseModel):
    name: str
    age: int
    height: float
    degrees: list[str]


person = Person(name="George", age=88, height=198, degrees=['BA', 'MBA', 'PhD'])

print(person.model_dump_json(indent=4))

print(person)
print(person.name)
print(person.degrees)