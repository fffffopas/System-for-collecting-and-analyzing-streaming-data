# generation/defaults.py
from __future__ import annotations

ROLES = ("carry", "mid", "offlane", "soft_support", "hard_support")

REGION_MMR_MEAN: dict[str, int] = {
    "EU": 3500,
    "NA": 3200,
    "SEA": 3000,
    "CN": 3400,
    "SA": 2800,
    "CIS": 3300,
}

# Границы MMR игрока (при генерации игроков и при обновлении после матча).
MMR_MIN = 0
MMR_MAX = 14000

# Страны игроков по регионам: {регион: {код страны ISO 3166-1 alpha-2: вес}}.
# Вес - относительная доля игроков региона из этой страны (не обязан давать сумму 1).
# Набор регионов должен совпадать с REGION_MMR_MEAN (проверяется тестом).
COUNTRY_WEIGHTS_BY_REGION: dict[str, dict[str, float]] = {
    "EU": {
        "DE": 0.22,
        "FR": 0.14,
        "PL": 0.12,
        "GB": 0.10,
        "ES": 0.09,
        "SE": 0.08,
        "IT": 0.07,
        "NL": 0.06,
        "FI": 0.04,
        "RO": 0.04,
        "DK": 0.04,
    },
    "NA": {"US": 0.80, "CA": 0.20},
    "SEA": {"SG": 0.15, "MY": 0.20, "TH": 0.18, "PH": 0.20, "ID": 0.17, "VN": 0.10},
    "CN": {"CN": 0.90, "HK": 0.04, "TW": 0.06},
    "SA": {"BR": 0.55, "AR": 0.14, "CL": 0.10, "PE": 0.11, "CO": 0.10},
    "CIS": {"RU": 0.50, "UA": 0.18, "KZ": 0.14, "BY": 0.08, "UZ": 0.06, "GE": 0.04},
}
DEFAULT_COUNTRY = "XX"

ROLE_KILLS_BASE: dict[str, float] = {
    "carry": 9.0,
    "mid": 8.0,
    "offlane": 6.0,
    "soft_support": 4.5,
    "hard_support": 3.0,
}
ROLE_DEATHS_BASE: dict[str, float] = {
    "carry": 4.0,
    "mid": 4.5,
    "offlane": 5.5,
    "soft_support": 6.0,
    "hard_support": 6.5,
}
ROLE_ASSISTS_BASE: dict[str, float] = {
    "carry": 5.0,
    "mid": 6.0,
    "offlane": 8.0,
    "soft_support": 11.0,
    "hard_support": 13.0,
}

DEFAULT_ROLE_WEIGHTS: tuple[float, ...] = (1, 1, 1, 1, 1)
DEFAULT_GPM = 450.0
DEFAULT_XPM = 520.0

# --- Архетипы: (веса ролей в порядке ROLES, средний GPM, средний XPM) ---
ARCHETYPES: dict[str, tuple[tuple[float, ...], float, float]] = {
    "carry": ((10, 1, 0, 0, 0), 590, 620),
    "carry_mid": ((6, 6, 1, 0, 0), 560, 610),
    "mid": ((1, 10, 1, 0, 0), 540, 620),
    "mid_offlane": ((0, 5, 5, 1, 0), 480, 570),
    "flex_core": ((4, 3, 4, 0, 0), 500, 580),
    "offlane": ((0, 1, 10, 1, 0), 440, 540),
    "offlane_support": ((0, 0, 4, 6, 2), 380, 480),
    "soft_support": ((0, 1, 0, 10, 3), 350, 450),
    "support": ((0, 0, 0, 6, 6), 320, 420),
    "hard_support": ((0, 0, 0, 2, 10), 290, 380),
}

# --- Герой -> архетип ---
HERO_ARCHETYPE: dict[str, str] = {
    # Strength
    "Abaddon": "support",
    "Alchemist": "carry",
    "Axe": "offlane",
    "Beastmaster": "offlane",
    "Brewmaster": "offlane",
    "Bristleback": "offlane",
    "Centaur Warrunner": "offlane",
    "Chaos Knight": "carry",
    "Clockwerk": "offlane_support",
    "Dawnbreaker": "offlane",
    "Doom": "offlane",
    "Dragon Knight": "flex_core",
    "Earth Spirit": "offlane_support",
    "Earthshaker": "offlane_support",
    "Elder Titan": "offlane_support",
    "Huskar": "carry_mid",
    "Io": "hard_support",
    "Kunkka": "flex_core",
    "Legion Commander": "offlane",
    "Lifestealer": "carry",
    "Lycan": "carry",
    "Magnus": "offlane",
    "Marci": "offlane_support",
    "Mars": "offlane",
    "Night Stalker": "offlane",
    "Omniknight": "support",
    "Phoenix": "offlane_support",
    "Pudge": "offlane_support",
    "Primal Beast": "offlane",
    "Sand King": "offlane_support",
    "Slardar": "offlane",
    "Spirit Breaker": "offlane_support",
    "Sven": "carry",
    "Tidehunter": "offlane",
    "Timbersaw": "mid_offlane",
    "Tiny": "flex_core",
    "Treant Protector": "hard_support",
    "Tusk": "offlane_support",
    "Underlord": "offlane",
    "Undying": "support",
    "Wraith King": "carry",
    # Agility
    "Anti-Mage": "carry",
    "Arc Warden": "carry_mid",
    "Bloodseeker": "flex_core",
    "Bounty Hunter": "soft_support",
    "Broodmother": "mid_offlane",
    "Clinkz": "carry_mid",
    "Drow Ranger": "carry",
    "Ember Spirit": "mid",
    "Faceless Void": "carry",
    "Gyrocopter": "carry",
    "Hoodwink": "soft_support",
    "Juggernaut": "carry",
    "Kez": "carry",
    "Lone Druid": "carry_mid",
    "Luna": "carry",
    "Medusa": "carry",
    "Meepo": "carry_mid",
    "Mirana": "support",
    "Monkey King": "carry_mid",
    "Morphling": "carry",
    "Naga Siren": "carry",
    "Nyx Assassin": "soft_support",
    "Pangolier": "mid_offlane",
    "Phantom Assassin": "carry",
    "Phantom Lancer": "carry",
    "Razor": "flex_core",
    "Riki": "carry",
    "Shadow Fiend": "mid",
    "Slark": "carry",
    "Sniper": "carry_mid",
    "Spectre": "carry",
    "Templar Assassin": "carry_mid",
    "Terrorblade": "carry",
    "Troll Warlord": "carry",
    "Ursa": "carry",
    "Vengeful Spirit": "soft_support",
    "Venomancer": "support",
    "Viper": "mid_offlane",
    "Weaver": "carry_mid",
    # Intelligence
    "Ancient Apparition": "hard_support",
    "Bane": "support",
    "Batrider": "mid_offlane",
    "Chen": "hard_support",
    "Crystal Maiden": "hard_support",
    "Dark Seer": "offlane",
    "Dark Willow": "support",
    "Dazzle": "support",
    "Death Prophet": "mid_offlane",
    "Disruptor": "support",
    "Enchantress": "support",
    "Enigma": "offlane_support",
    "Grimstroke": "support",
    "Invoker": "mid",
    "Jakiro": "support",
    "Keeper of the Light": "support",
    "Largo": "support",
    "Leshrac": "mid",
    "Lich": "hard_support",
    "Lina": "carry_mid",
    "Lion": "support",
    "Muerta": "carry_mid",
    "Nature's Prophet": "flex_core",
    "Necrophos": "mid_offlane",
    "Ogre Magi": "soft_support",
    "Oracle": "hard_support",
    "Outworld Destroyer": "mid",
    "Puck": "mid",
    "Pugna": "mid_offlane",
    "Queen of Pain": "mid",
    "Ringmaster": "support",
    "Rubick": "soft_support",
    "Shadow Demon": "support",
    "Shadow Shaman": "hard_support",
    "Silencer": "support",
    "Skywrath Mage": "support",
    "Snapfire": "support",
    "Storm Spirit": "mid",
    "Techies": "support",
    "Tinker": "mid",
    "Visage": "mid_offlane",
    "Void Spirit": "mid",
    "Warlock": "hard_support",
    "Windranger": "flex_core",
    "Winter Wyvern": "hard_support",
    "Witch Doctor": "hard_support",
    "Zeus": "mid",
}

SIDES = ("radiant", "dire")
SIDE_WIN_BONUS: dict[str, float] = {"radiant": 0.01, "dire": -0.01}

# Бонус к винрейту героя относительно «среднего героя» меты.
#
# Источник: DotaPicker (https://dotapicker.com/pubmeta), патч 7.41, срез от 15.11.2026,
# ranked All Pick, весь матч, среднее по трём группам рейтинга (Normal/High/Very High).
# Формула: (винрейт героя - средний винрейт по всем героям) / 100.
# Среднее по мете ≈ 49.43%, поэтому центрируем на него, а не на 50%: иначе у синтетических
# данных общий винрейт «поплыл» бы вниз (~49%). Сумма бонусов ≈ 0.
# В комментарии справа - исходный винрейт героя в мете. Отсортировано от сильных к слабым.
# При смене патча: обновить значения и дату выше (пересчитать по таблице меты).
HERO_WINRATE_BONUS: dict[str, float] = {
    "Wraith King": +0.053,  # 54.7%
    "Meepo": +0.047,  # 54.1%
    "Visage": +0.044,  # 53.8%
    "Outworld Destroyer": +0.038,  # 53.2%
    "Riki": +0.037,  # 53.1%
    "Spectre": +0.036,  # 53.0%
    "Juggernaut": +0.034,  # 52.8%
    "Nyx Assassin": +0.033,  # 52.7%
    "Phantom Lancer": +0.033,  # 52.7%
    "Arc Warden": +0.032,  # 52.6%
    "Dragon Knight": +0.032,  # 52.6%
    "Bounty Hunter": +0.031,  # 52.5%
    "Legion Commander": +0.031,  # 52.5%
    "Lich": +0.031,  # 52.5%
    "Grimstroke": +0.029,  # 52.3%
    "Dawnbreaker": +0.028,  # 52.2%
    "Phoenix": +0.027,  # 52.1%
    "Vengeful Spirit": +0.027,  # 52.1%
    "Witch Doctor": +0.027,  # 52.1%
    "Night Stalker": +0.026,  # 52.0%
    "Spirit Breaker": +0.026,  # 52.0%
    "Bloodseeker": +0.024,  # 51.8%
    "Shadow Shaman": +0.022,  # 51.6%
    "Enigma": +0.021,  # 51.5%
    "Lifestealer": +0.021,  # 51.5%
    "Mirana": +0.021,  # 51.5%
    "Sven": +0.021,  # 51.5%
    "Ancient Apparition": +0.020,  # 51.4%
    "Troll Warlord": +0.020,  # 51.4%
    "Abaddon": +0.019,  # 51.3%
    "Leshrac": +0.019,  # 51.3%
    "Omniknight": +0.019,  # 51.3%
    "Brewmaster": +0.018,  # 51.2%
    "Crystal Maiden": +0.018,  # 51.2%
    "Dazzle": +0.018,  # 51.2%
    "Pudge": +0.018,  # 51.2%
    "Anti-Mage": +0.017,  # 51.1%
    "Invoker": +0.017,  # 51.1%
    "Techies": +0.015,  # 50.9%
    "Chaos Knight": +0.014,  # 50.8%
    "Elder Titan": +0.013,  # 50.7%
    "Pugna": +0.013,  # 50.7%
    "Earthshaker": +0.012,  # 50.6%
    "Phantom Assassin": +0.012,  # 50.6%
    "Disruptor": +0.011,  # 50.5%
    "Necrophos": +0.011,  # 50.5%
    "Broodmother": +0.009,  # 50.3%
    "Clinkz": +0.009,  # 50.3%
    "Luna": +0.009,  # 50.3%
    "Oracle": +0.007,  # 50.1%
    "Razor": +0.007,  # 50.1%
    "Io": +0.006,  # 50.0%
    "Ogre Magi": +0.006,  # 50.0%
    "Silencer": +0.006,  # 50.0%
    "Axe": +0.005,  # 49.9%
    "Undying": +0.005,  # 49.9%
    "Zeus": +0.005,  # 49.9%
    "Dark Seer": +0.003,  # 49.7%
    "Marci": +0.003,  # 49.7%
    "Primal Beast": +0.003,  # 49.7%
    "Slark": +0.003,  # 49.7%
    "Keeper of the Light": +0.002,  # 49.6%
    "Skywrath Mage": +0.002,  # 49.6%
    "Void Spirit": +0.002,  # 49.6%
    "Warlock": +0.002,  # 49.6%
    "Rubick": +0.001,  # 49.5%
    "Winter Wyvern": +0.001,  # 49.5%
    "Bane": +0.000,  # 49.4%
    "Lone Druid": +0.000,  # 49.4%
    "Lycan": +0.000,  # 49.4%
    "Naga Siren": +0.000,  # 49.4%
    "Earth Spirit": -0.001,  # 49.3%
    "Magnus": -0.001,  # 49.3%
    "Snapfire": -0.002,  # 49.2%
    "Dark Willow": -0.003,  # 49.1%
    "Kunkka": -0.003,  # 49.1%
    "Sniper": -0.003,  # 49.1%
    "Sand King": -0.004,  # 49.0%
    "Centaur Warrunner": -0.005,  # 48.9%
    "Slardar": -0.005,  # 48.9%
    "Medusa": -0.006,  # 48.8%
    "Ursa": -0.006,  # 48.8%
    "Venomancer": -0.006,  # 48.8%
    "Ember Spirit": -0.007,  # 48.7%
    "Tidehunter": -0.007,  # 48.7%
    "Death Prophet": -0.008,  # 48.6%
    "Lion": -0.009,  # 48.5%
    "Viper": -0.009,  # 48.5%
    "Faceless Void": -0.010,  # 48.4%
    "Largo": -0.010,  # 48.4%
    "Ringmaster": -0.010,  # 48.4%
    "Doom": -0.012,  # 48.2%
    "Windranger": -0.012,  # 48.2%
    "Jakiro": -0.013,  # 48.1%
    "Tusk": -0.014,  # 48.0%
    "Mars": -0.015,  # 47.9%
    "Clockwerk": -0.016,  # 47.8%
    "Underlord": -0.016,  # 47.8%
    "Morphling": -0.017,  # 47.7%
    "Muerta": -0.017,  # 47.7%
    "Tinker": -0.017,  # 47.7%
    "Enchantress": -0.020,  # 47.4%
    "Hoodwink": -0.021,  # 47.3%
    "Queen of Pain": -0.021,  # 47.3%
    "Weaver": -0.021,  # 47.3%
    "Bristleback": -0.022,  # 47.2%
    "Gyrocopter": -0.024,  # 47.0%
    "Lina": -0.024,  # 47.0%
    "Puck": -0.024,  # 47.0%
    "Storm Spirit": -0.024,  # 47.0%
    "Pangolier": -0.032,  # 46.2%
    "Alchemist": -0.033,  # 46.1%
    "Chen": -0.034,  # 46.0%
    "Drow Ranger": -0.036,  # 45.8%
    "Templar Assassin": -0.036,  # 45.8%
    "Beastmaster": -0.038,  # 45.6%
    "Huskar": -0.038,  # 45.6%
    "Monkey King": -0.038,  # 45.6%
    "Timbersaw": -0.039,  # 45.5%
    "Kez": -0.040,  # 45.4%
    "Treant Protector": -0.040,  # 45.4%
    "Terrorblade": -0.045,  # 44.9%
    "Tiny": -0.049,  # 44.5%
    "Shadow Demon": -0.050,  # 44.4%
    "Batrider": -0.051,  # 44.3%
    "Nature's Prophet": -0.064,  # 43.0%
    "Shadow Fiend": -0.067,  # 42.7%
}

DEFAULT_HERO_WINRATE_BONUS = 0.0

OVERRIDES: dict[str, tuple[float, float]] = {
    "Anti-Mage": (620, 650),
    "Alchemist": (650, 600),
    "Medusa": (620, 600),
    "Morphling": (600, 640),
    "Spectre": (600, 620),
    "Meepo": (580, 650),
    "Lone Druid": (500, 560),
    "Invoker": (560, 640),
    "Tinker": (580, 620),
    "Pudge": (400, 520),
    "Crystal Maiden": (280, 360),
    "Chen": (260, 340),
}

# для DotaProfile
HERO_ROLE_WEIGHTS: dict[str, tuple[float, ...]] = {}
HERO_GPM_MEAN: dict[str, float] = {}
HERO_XPM_MEAN: dict[str, float] = {}

for _hero, _arch in HERO_ARCHETYPE.items():
    _weights, _gpm, _xpm = ARCHETYPES[_arch]
    HERO_ROLE_WEIGHTS[_hero] = _weights
    HERO_GPM_MEAN[_hero], HERO_XPM_MEAN[_hero] = OVERRIDES.get(_hero, (_gpm, _xpm))

ALL_HEROES: list[str] = sorted(HERO_ARCHETYPE)
