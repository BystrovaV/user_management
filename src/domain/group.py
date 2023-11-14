from dataclasses import dataclass
from datetime import datetime


@dataclass
class Group:
    id: int
    name: str | None = None
    created_at: datetime | None = None
