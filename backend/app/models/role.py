from enum import Enum


class RoleName(str, Enum):
    SUPER_ADMIN = "super_admin"
    TEAM_MEMBER = "team_member"
    USER = "user"