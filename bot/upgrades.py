import math
import typing as t
from enum import Enum, auto


class Upgrades(Enum):
    ROLL_REGEN = auto()
    """Increases the regeration speed of rolls."""
    ROLL_MAX = auto()
    DAILY_BONUS = auto()
    FRAGMENT_BONUS = auto()
    WISHLIST_SIZE = auto()
    WISHLIST_RATE_BONUS = auto()
    UPGRADE_6 = auto()
    UPGRADE_7 = auto()
    UPGRADE_8 = auto()
    UPGRADE_9 = auto()


UpgradeFunctions = t.Tuple[t.Callable[[float], float], t.Callable[[float], str]]


def roll_generation_rate_modifier(level) -> int:
    return 900 - level * 60


def roll_generation_rate_formatted_modifier(level) -> str:
    minutes = int((roll_generation_rate_modifier(level) / 60) % 60)
    return f"{minutes} minutes"


def roll_maximum_modifier(level) -> int:
    return 20 + level * 3


def roll_maximum_formatted_modifier(level) -> str:
    return f"{roll_maximum_modifier(level)} rolls"


def daily_bonus_modifier(level) -> int:
    return 5 + level


def daily_bonus_formatted_modifier(level) -> str:
    return f"{daily_bonus_modifier(level)}"


def fragment_bonus_modifier(level) -> float:
    return 1 + level * 0.2


def fragment_bonus_formatted_modifier(level) -> str:
    return f"{fragment_bonus_modifier(level)}x"


def wishlist_size_modifier(level) -> int:
    return 7 + level


def wishlist_size_formatted_modifier(level) -> str:
    return f"{wishlist_size_modifier(level)} slots"


def modifier_as_int(level) -> int:
    return int((math.log(level + 1, 1.62) / 2387) * 10000 + 0.5)


def wishlist_rate_bonus_modifier(level) -> float:
    return modifier_as_int(level) / 10000


def wishlist_rate_bonus_formatted_modifier(level) -> str:
    if level != 0:
        return f"1 in {int(10000 / modifier_as_int(level))} rolls"
    return "1 in 20000 rolls"


class UpgradeEffects:
    upgrades: dict[Upgrades, UpgradeFunctions] = {
        Upgrades.ROLL_REGEN: (roll_generation_rate_modifier, roll_generation_rate_formatted_modifier),
        Upgrades.ROLL_MAX: (roll_maximum_modifier, roll_maximum_formatted_modifier),
        Upgrades.DAILY_BONUS: (daily_bonus_modifier, daily_bonus_formatted_modifier),
        Upgrades.FRAGMENT_BONUS: (fragment_bonus_modifier, fragment_bonus_formatted_modifier),
        Upgrades.WISHLIST_SIZE: (wishlist_size_modifier, wishlist_size_formatted_modifier),
        Upgrades.WISHLIST_RATE_BONUS: (wishlist_rate_bonus_modifier, wishlist_rate_bonus_formatted_modifier),
    }
