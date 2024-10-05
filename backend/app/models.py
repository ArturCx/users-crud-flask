from dataclasses import dataclass

@dataclass
class UserPreferences:
    timezone: str

@dataclass
class User:
    username: str
    password: str
    roles: list
    preferences: UserPreferences
    active: bool = True
    created_ts: float = 0.0