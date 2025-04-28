from datetime import datetime
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query

from chores_completions.repository import ChoreMetricRepository
from chores_completions.schemas import ChoresFamilyCount, DateRange, UserChoresCount

router = APIRouter()


def get_date_range(
    start: Optional[datetime] = Query(
        None, description="Start date of the interval (inclusive)"
    ),
    end: Optional[datetime] = Query(
        None, description="End date of the interval (inclusive)"
    ),
):
    return DateRange(start=start, end=end)


date_range_docs = """
- **family_id** — The ID of the family (required).
- **start** — Start date of the interval (optional). If not provided, there will be no lower time limit.
- **end** — End date of the interval (optional). If not provided, there will be no upper time limit.

If both start and end dates are missing, the statistics are calculated for all time.
"""


@router.get(
    "/stats/families/{family_id}/members",
    response_model=list[UserChoresCount],
    summary="Get family members' chore completion stats",
    description=f"""
        Returns a list of family members along with the number of chores they have completed within a specified date range.
        {date_range_docs}
    The results are ordered by the number of completed chores in descending order.
    """,
)
async def family_members_stats(
    family_id: UUID,
    interval: DateRange = Depends(get_date_range),
) -> list[UserChoresCount]:
    result = await ChoreMetricRepository().get_family_members_by_chores_completions(
        family_id, interval
    )
    return result


@router.get(
    "/stats/families/{family_id}/chores",
    response_model=list[ChoresFamilyCount],
    summary="Get family chores with number of completions",
    description=f"""
        Returns a list of family chores along with the number of chores completed by family members within a specified date range.
        {date_range_docs}
    The results are ordered by the number of completed chores in descending order.
    """,
)
async def family_chores_stats(
    family_id: UUID,
    interval: DateRange = Depends(get_date_range),
) -> list[ChoresFamilyCount]:
    result = await ChoreMetricRepository().get_family_chores_by_completions(
        family_id, interval
    )
    return result
