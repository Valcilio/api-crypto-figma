from dataclasses import dataclass

@dataclass
class Currencies:
    timestamp: str
    high: float
    low: float
    close: float
    open: float
    market_cap: float