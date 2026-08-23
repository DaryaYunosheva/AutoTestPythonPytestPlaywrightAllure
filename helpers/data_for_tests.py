from dataclasses import dataclass


@dataclass
class User:
    first_name: str
    last_name: str
    email: str
    phone: str
    password: str

user1 = User("Tester", "Tester", "test@example.com", "+71112223341", "password123")
user2 = User("Darya", "Tester", "darya@darya.ru", "111222333444", "qwerty123")