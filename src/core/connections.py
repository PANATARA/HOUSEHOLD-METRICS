import clickhouse_connect as ch

import config
from core.singleton import Singleton

__all__ = ["get_click_house_client"]


class _ClickHouseClient(metaclass=Singleton):
    def __init__(self):
        self.click_house_url = config.CLICKHOUSE_HOST
        self.CLICKHOUSE_PORT = config.CLICKHOUSE_PORT
        self.CLICKHOUSE_USER = config.CLICKHOUSE_USER
        self.CLICKHOUSE_PASSWORD = config.CLICKHOUSE_PASSWORD
        self._client = None

    async def get_client(self):
        if self._client is None:
            self._client = await ch.get_async_client(
                host=self.click_house_url,
                username=self.CLICKHOUSE_USER,
                port=self.CLICKHOUSE_PORT,
                password=self.CLICKHOUSE_PASSWORD,
            )
        return self._client


_click_house_client = _ClickHouseClient()


async def get_click_house_client():
    return await _click_house_client.get_client()
