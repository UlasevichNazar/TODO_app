import enum


# for User model
class Roles(str, enum.Enum):
    ROLE_USER = "USER"
    ROLE_ADMIN = "ADMIN"


# for Task model
class TaskStatus(str, enum.Enum):
    IN_PROGRESS = "In progress"
    DONE = "Done"
