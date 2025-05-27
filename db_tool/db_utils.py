from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import asyncio

async def extract_metadata(uri: str) -> str:
    engine = create_async_engine(uri)
    async with engine.connect() as conn:
        db_type = uri.split(":")[0]

        if db_type.startswith("postgresql"):
            query = """
            SELECT table_name, column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = 'public'
            ORDER BY table_name, ordinal_position;
            """
        elif db_type.startswith("mysql"):
            query = """
            SELECT table_name, column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = DATABASE()
            ORDER BY table_name, ordinal_position;
            """
        elif db_type.startswith("sqlite"):
            query = """
            SELECT m.name AS table_name, p.name AS column_name, p.type AS data_type
            FROM sqlite_master m
            JOIN pragma_table_info(m.name) p
            ON m.name NOT LIKE 'sqlite_%'
            WHERE m.type = 'table';
            """
        else:
            raise ValueError(f"Unsupported DB type: {db_type}")

        result = await conn.execute(text(query))
        rows = result.fetchall()

    # Build schema string
    schema = {}
    for table, column, dtype in rows:
        schema.setdefault(table, []).append(f"{column} {dtype}")
    
    formatted = "\n".join(f"{tbl}({', '.join(cols)})" for tbl, cols in schema.items())
    return formatted

async def run_query(uri: str, query: str):
    engine = create_async_engine(uri, echo=False)
    async with engine.connect() as conn:
        result = await conn.execute(text(query))
        rows = result.mappings().all()
        await conn.close()
        return rows