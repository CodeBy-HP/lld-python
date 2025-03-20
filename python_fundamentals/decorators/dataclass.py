# A @dataclass is a decorator in Python that automatically generates methods like __init__(), __repr__(), __eq__(), etc., for a class. 

# For setting the Configuration for our code

from dataclasses import dataclass


@dataclass
class User:
    id: int
    username: str
    email: str

# Example API response
data = User(101, "coder123", "coder@example.com")
print(data.username)  # coder123
