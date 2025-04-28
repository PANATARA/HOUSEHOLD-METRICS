from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class DateRange(BaseModel):
    start: datetime | None
    end: datetime | None


class UserChoresCount(BaseModel):
    user_id: UUID
    chores_completions_counts: int
