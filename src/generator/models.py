import enum
from datetime import datetime, timedelta
from dataclasses import dataclass

@dataclass(frozen=True, slots = True)
class Player:
    player_id: int
    nickname: str
    country: str
    region: str
    registred_at: datetime

@dataclass(frozen=True, slots = True)
class Hero:
    hero_id: int
    hero_name: str
    hero_role: str

@dataclass(frozen=True, slots = True)
class TableFacts: 
    match_id: int
    player_id: int
    hero_id: int
    match_time: timedelta
    result: bool
    mmr_before: int
    mmr_delta: int
    gpm: float
    xpm: float
    kills: int 
    deaths: int 
    assist: int

    #----В аномалии----
    rampage: bool
    abandoned: bool
    report_received: bool
    commend_received: bool
    entered_low_prioriry: bool




