from datetime import datetime, timedelta, date
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query

from chores_completions.repository import ChoreMetricRepository
from chores_completions.schemas import (
    ActivitySchema,
    ChoresFamilyCountSchema,
    DateRangeSchema,
    UserActivitySchema,
    UserChoresCountSchema,
)

router = APIRouter()


def get_date_range(
    start: Optional[datetime] = Query(
        None, description="Start date of the interval (inclusive)"
    ),
    end: Optional[datetime] = Query(
        None, description="End date of the interval (inclusive)"
    ),
):
    return DateRangeSchema(start=start, end=end)


def get_list_activities(
    activity_data: dict[date, int], interval: DateRangeSchema
) -> list[ActivitySchema]:
    data_keys = list(activity_data.keys())
    first_key, last_key = data_keys[0], data_keys[-1]

    start = interval.start.date() if interval.start else first_key
    end = interval.end.date() if interval.end else last_key

    all_dates = {start + timedelta(days=i): 0 for i in range((end - start).days + 1)}

    for key, value in activity_data.items():
        all_dates[key] = value

    activities = [
        ActivitySchema(activity_date=day, activity=count)
        for day, count in sorted(all_dates.items())
    ]
    return activities


date_range_docs = """
- **start** — Start date of the interval (optional). If not provided, there will be no lower time limit.
- **end** — End date of the interval (optional). If not provided, there will be no upper time limit.

If both start and end dates are missing, the statistics are calculated for all time.
"""


@router.get(
    "/stats/families/{family_id}/members",
    response_model=list[UserChoresCountSchema],
    summary="Get family members' chore completion stats",
    description=f"""
        Returns a list of family members along with the number of chores they have completed within a specified date range.
        - **family_id** — The ID of the family (required).
        {date_range_docs}
    The results are ordered by the number of completed chores in descending order.
    """,
)
async def family_members_stats(
    family_id: UUID,
    interval: DateRangeSchema = Depends(get_date_range),
) -> list[UserChoresCountSchema]:
    result = await ChoreMetricRepository().get_family_members_by_chores_completions(
        family_id, interval
    )
    return result


@router.get(
    "/stats/families/{family_id}/chores",
    response_model=list[ChoresFamilyCountSchema],
    summary="Get family chores with number of completions",
    description=f"""
        Returns a list of family chores along with the number of chores completed by family members within a specified date range.
        - **family_id** — The ID of the family (required).
        {date_range_docs}
    The results are ordered by the number of completed chores in descending order.
    """,
)
async def family_chores_stats(
    family_id: UUID,
    interval: DateRangeSchema = Depends(get_date_range),
) -> list[ChoresFamilyCountSchema]:
    result = await ChoreMetricRepository().get_family_chores_by_completions(
        family_id, interval
    )
    return result


@router.get(
    "/stats/families/{family_id}/activity",
    response_model=UserActivitySchema,
    summary="---",
    description=f"""
Retrieves the family's daily activity statistics within a specified date range.

Each day in the range will be listed, even if the nobody had no activity on that day (activity count will be 0).

**Path parameters**:
- **family_id** — Unique identifier of the family (required).

**Query parameters**:
{date_range_docs}

**Response**:
Returns a list of days with the corresponding number of completed chores.  
Days without any activity will have an activity count of 0.
Results are sorted chronologically.

**Note:**  
- The maximum allowed date range is **1 year** (366 days).  
- If a longer range is requested, an error will be returned.
""",
)
async def family_activity(
    family_id: UUID,
    interval: DateRangeSchema = Depends(get_date_range),
) -> UserActivitySchema:
    if (interval.end - interval.start).days > 366:
        raise HTTPException(
            status_code=422, detail="Date range too large, max 1 year allowed."
        )

    activity_data = await ChoreMetricRepository().get_family_activity(
        family_id, interval
    )
    if not activity_data:
        return UserActivitySchema(activities=[])

    list_activities = get_list_activities(activity_data, interval)

    return UserActivitySchema(activities=list_activities)


@router.get(
    "/stats/user/{completed_by_id}/activity",
    response_model=UserActivitySchema,
    summary="Get user's daily activity",
    description=f"""
Retrieves the user's daily activity statistics within a specified date range.

Each day in the range will be listed, even if the user had no activity on that day (activity count will be 0).

**Path parameters**:
- **user_id** — Unique identifier of the user (required).

**Query parameters**:
{date_range_docs}

**Response**:
Returns a list of days with the corresponding number of completed chores.  
Days without any activity will have an activity count of 0.
Results are sorted chronologically.

**Note:**  
- The maximum allowed date range is **1 year** (366 days).  
- If a longer range is requested, an error will be returned.
""",
)
async def user_activity(
    completed_by_id: UUID,
    interval: DateRangeSchema = Depends(get_date_range),
) -> UserActivitySchema:
    if (interval.end - interval.start).days > 366:
        raise HTTPException(
            status_code=422, detail="Date range too large, max 1 year allowed."
        )

    activity_data = await ChoreMetricRepository().get_family_member_activity(
        completed_by_id, interval
    )

    if not activity_data:
        return UserActivitySchema(activities=[])

    list_activities = get_list_activities(activity_data, interval)

    return UserActivitySchema(activities=list_activities)


@router.get(
    "/stats/user/{completed_by_id}/counts",
    response_model=UserChoresCountSchema,
    summary="Get family chores with number of completions",
    description=f"""
        Returns the total number of completed chores by a specific user within a given date range.
        - **completed_by_id** — The ID of the user whose completions are being counted.
        {date_range_docs}
    If the date range is not provided, all chore completions by the user will be counted.
    """,
)
async def users_chores_counts(
    completed_by_id: UUID,
    interval: DateRangeSchema = Depends(get_date_range),
) -> UserChoresCountSchema:
    result = await ChoreMetricRepository().get_user_chore_completion_count(
        completed_by_id, interval
    )
    return UserChoresCountSchema(user_id=result[0], chores_completions_counts=result[1])
