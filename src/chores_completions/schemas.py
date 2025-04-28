from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class DateRange(BaseModel):
    start: datetime | None = Field(None, description="Start date of the interval (inclusive)")
    end: datetime | None= Field(None, description="End date of the interval (inclusive)")


class UserChoresCount(BaseModel):
    user_id: UUID
    chores_completions_counts: int


class ChoresFamilyCount(BaseModel):
    chore_id: UUID
    chores_completions_counts: int
