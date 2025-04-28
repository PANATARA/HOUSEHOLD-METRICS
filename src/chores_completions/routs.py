from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Query

from chores_completions.repository import ChoreAnalyticRepository
from chores_completions.schemas import DateRange, UserChoresCount

router = APIRouter()


@router.get(
    "/stats/families/members",
    response_model=list[UserChoresCount],
    summary="Get family members' chore completion stats",
    description="""
Returns a list of family members along with the number of chores they have completed within a specified date range.

- **family_id** — The ID of the family (required).
- **start** — Start date of the interval (optional). If not provided, there will be no lower time limit.
- **end** — End date of the interval (optional). If not provided, there will be no upper time limit.

If both start and end dates are missing, the statistics are calculated for all time.

The results are ordered by the number of completed chores in descending order.
""",
)
async def family_members_stats(
    family_id: UUID = Query(..., description="Family ID"),
    start: datetime | None = Query(
        None, description="Start date of the interval (inclusive)"
    ),
    end: datetime | None = Query(
        None, description="End date of the interval (inclusive)"
    ),
) -> list[UserChoresCount]:
    interval = DateRange(start=start, end=end)
    result = await ChoreAnalyticRepository().get_family_members_by_chores_completions(
        family_id, interval
    )
    return result
