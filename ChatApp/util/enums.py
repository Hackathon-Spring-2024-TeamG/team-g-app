from enum import Enum, unique

@unique
class AssociableType(Enum):
    MESSAGE = 'message'
    PERSONAL_MESSAGE = 'personal_message'

@unique
class BadgeType(Enum):
    FAST_PARROT = 'fast_parrot'
    ANGEL_PARROT = 'angel_parrot'