from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class GitRepo:
    name: str
    path: str
    branch: str
    last_updated: datetime
    health_score: float
    commits: List['Commit']
    alerts: List['Alert']

@dataclass
class Commit:
    hash: str
    message: str
    author: str
    date: str

@dataclass
class Alert:
    level: str  # 'critical', 'warning', 'info'
    message: str