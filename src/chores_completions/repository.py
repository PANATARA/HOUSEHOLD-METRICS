from uuid import UUID

from chores_completions.schemas import DateRange, UserChoresCount
from core.connections import get_click_house_client


class ChoreAnalyticRepository:
    async def get_family_members_by_chores_completions(
        self,
        family_id: UUID,
        interval: DateRange | None = None,
    ) -> list[UserChoresCount]:
        async_client = await get_click_house_client()

        condition = "family_id = %(family_id)s"
        parameters = {"family_id": str(family_id)}

        if interval:
            if interval.start and interval.end:
                condition += " AND created_at BETWEEN %(start_date)s AND %(end_date)s"
                parameters["start_date"] = interval.start
                parameters["end_date"] = interval.end
            elif interval.start:
                condition += " AND created_at >= %(start_date)s"
                parameters["start_date"] = interval.start
            elif interval.end:
                condition += " AND created_at <= %(end_date)s"
                parameters["end_date"] = interval.end

        query_result = await async_client.query(
            query=f"""
                SELECT 
                    completed_by_id, 
                    count(*) AS chore_completion_count
                FROM chore_completion_stats
                WHERE {condition}
                GROUP BY completed_by_id
                ORDER BY chore_completion_count DESC
            """,
            parameters=parameters,
        )

        return [
            UserChoresCount(user_id=row[0], chores_completions_counts=row[1])
            for row in query_result.result_rows
        ]
