from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(slots = True)
class Player:
    player_id: int
    mmr: int
    nickname: str
    country: str
    region: str
    registered_at: datetime

@dataclass(frozen=True, slots = True)
class Hero:
    hero_id: int
    hero_name: str

@dataclass(frozen=True, slots = True)
class TableFacts: 
    match_id: int
    player_id: int
    hero_id: int

    side: str
    role: str
    match_time: timedelta
    result: bool
    mmr_delta: int
    gpm: float
    xpm: float
    kills: int 
    deaths: int 
    assists: int # assist -> assists

    #----В аномалии----
    rampage: bool
    abandoned: bool
    report_received: bool
    commend_received: bool
    entered_low_priority: bool




