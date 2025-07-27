# security.py
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"
    GUEST = "guest"
