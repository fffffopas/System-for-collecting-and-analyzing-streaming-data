# generation/defaults.py
from __future__ import annotations

ROLES = ("carry", "mid", "offlane", "soft_support", "hard_support")

REGION_MMR_MEAN: dict[str, int] = {
    "EU": 3500, "NA": 3200, "SEA": 3000, "CN": 3400, "SA": 2800, "CIS": 3300,
}
print (list(REGION_MMR_MEAN))

ROLE_KILLS_BASE: dict[str, float] = {
    "carry": 9.0, "mid": 8.0, "offlane": 6.0, "soft_support": 4.5, "hard_support": 3.0,
}
ROLE_DEATHS_BASE: dict[str, float] = {
    "carry": 4.0, "mid": 4.5, "offlane": 5.5, "soft_support": 6.0, "hard_support": 6.5,
}
ROLE_ASSISTS_BASE: dict[str, float] = {
    "carry": 5.0, "mid": 6.0, "offlane": 8.0, "soft_support": 11.0, "hard_support": 13.0,
}

DEFAULT_ROLE_WEIGHTS: tuple[float, ...] = (1, 1, 1, 1, 1)
DEFAULT_GPM = 450.0
DEFAULT_XPM = 520.0

# --- Архетипы: (веса ролей в порядке ROLES, средний GPM, средний XPM) ---
ARCHETYPES: dict[str, tuple[tuple[float, ...], float, float]] = {
    "carry":           ((10, 1, 0, 0, 0), 590, 620),
    "carry_mid":       ((6, 6, 1, 0, 0),  560, 610),
    "mid":             ((1, 10, 1, 0, 0), 540, 620),
    "mid_offlane":     ((0, 5, 5, 1, 0),  480, 570),
    "flex_core":       ((4, 3, 4, 0, 0),  500, 580),
    "offlane":         ((0, 1, 10, 1, 0), 440, 540),
    "offlane_support": ((0, 0, 4, 6, 2),  380, 480),
    "soft_support":    ((0, 1, 0, 10, 3), 350, 450),
    "support":         ((0, 0, 0, 6, 6),  320, 420),
    "hard_support":    ((0, 0, 0, 2, 10), 290, 380),
}

# --- Герой -> архетип ---
HERO_ARCHETYPE: dict[str, str] = {
    # Strength
    "Abaddon": "support", "Alchemist": "carry", "Axe": "offlane",
    "Beastmaster": "offlane", "Brewmaster": "offlane", "Bristleback": "offlane",
    "Centaur Warrunner": "offlane", "Chaos Knight": "carry",
    "Clockwerk": "offlane_support", "Dawnbreaker": "offlane", "Doom": "offlane",
    "Dragon Knight": "flex_core", "Earth Spirit": "offlane_support",
    "Earthshaker": "offlane_support", "Elder Titan": "offlane_support",
    "Huskar": "carry_mid", "Io": "hard_support", "Kunkka": "flex_core",
    "Legion Commander": "offlane", "Lifestealer": "carry", "Lycan": "carry",
    "Magnus": "offlane", "Marci": "offlane_support", "Mars": "offlane",
    "Night Stalker": "offlane", "Omniknight": "support", "Phoenix": "offlane_support",
    "Pudge": "offlane_support", "Primal Beast": "offlane", "Sand King": "offlane_support",
    "Slardar": "offlane", "Spirit Breaker": "offlane_support", "Sven": "carry",
    "Tidehunter": "offlane", "Timbersaw": "mid_offlane", "Tiny": "flex_core",
    "Treant Protector": "hard_support", "Tusk": "offlane_support",
    "Underlord": "offlane", "Undying": "support", "Wraith King": "carry",
    # Agility
    "Anti-Mage": "carry", "Arc Warden": "carry_mid", "Bloodseeker": "flex_core",
    "Bounty Hunter": "soft_support", "Broodmother": "mid_offlane",
    "Clinkz": "carry_mid", "Drow Ranger": "carry", "Ember Spirit": "mid",
    "Faceless Void": "carry", "Gyrocopter": "carry", "Hoodwink": "soft_support",
    "Juggernaut": "carry", "Kez": "carry", "Lone Druid": "carry_mid",
    "Luna": "carry", "Medusa": "carry", "Meepo": "carry_mid", "Mirana": "support",
    "Monkey King": "carry_mid", "Morphling": "carry", "Naga Siren": "carry",
    "Nyx Assassin": "soft_support", "Pangolier": "mid_offlane",
    "Phantom Assassin": "carry", "Phantom Lancer": "carry", "Razor": "flex_core",
    "Riki": "carry", "Shadow Fiend": "mid", "Slark": "carry", "Sniper": "carry_mid",
    "Spectre": "carry", "Templar Assassin": "carry_mid", "Terrorblade": "carry",
    "Troll Warlord": "carry", "Ursa": "carry", "Vengeful Spirit": "soft_support",
    "Venomancer": "support", "Viper": "mid_offlane", "Weaver": "carry_mid",
    # Intelligence
    "Ancient Apparition": "hard_support", "Bane": "support", "Batrider": "mid_offlane",
    "Chen": "hard_support", "Crystal Maiden": "hard_support", "Dark Seer": "offlane",
    "Dark Willow": "support", "Dazzle": "support", "Death Prophet": "mid_offlane",
    "Disruptor": "support", "Enchantress": "support", "Enigma": "offlane_support",
    "Grimstroke": "support", "Invoker": "mid", "Jakiro": "support",
    "Keeper of the Light": "support", "Largo": "support", "Leshrac": "mid",
    "Lich": "hard_support", "Lina": "carry_mid", "Lion": "support",
    "Muerta": "carry_mid", "Nature's Prophet": "flex_core", "Necrophos": "mid_offlane",
    "Ogre Magi": "soft_support", "Oracle": "hard_support", "Outworld Destroyer": "mid",
    "Puck": "mid", "Pugna": "mid_offlane", "Queen of Pain": "mid",
    "Ringmaster": "support", "Rubick": "soft_support", "Shadow Demon": "support",
    "Shadow Shaman": "hard_support", "Silencer": "support", "Skywrath Mage": "support",
    "Snapfire": "support", "Storm Spirit": "mid", "Techies": "support",
    "Tinker": "mid", "Visage": "mid_offlane", "Void Spirit": "mid",
    "Warlock": "hard_support", "Windranger": "flex_core",
    "Winter Wyvern": "hard_support", "Witch Doctor": "hard_support", "Zeus": "mid",
}

SIDES = ("radiant", "dire")
SIDE_WIN_BONUS: dict[str, float] = {"radiant": 0.01, "dire": -0.01}

HERO_WINRATE_BONUS: dict[str, float] = {
    "Anti-Mage": -0.01, "Juggernaut": 0.02, "Axe": 0.01,
    "Pudge": -0.01, "Crystal Maiden": 0.00, "Invoker": -0.02,
    "Io": 0.02, "Treant Protector": 0.02, "Medusa": -0.01,
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