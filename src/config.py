import os

CLICKHOUSE_HOST: str = os.getenv("CLICKHOUSE_HOST", default="localhost")
CLICKHOUSE_PORT: int = int(os.getenv("CLICKHOUSE_PORT", default="8123"))
CLICKHOUSE_USER: str = os.getenv("CLICKHOUSE_USER", default="default")
CLICKHOUSE_PASSWORD: str = os.getenv("CLICKHOUSE_PASSWORD", default="clickhouse")
