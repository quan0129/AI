import typer
import asyncio
from tabulate import tabulate
from db_utils import run_query, extract_metadata
from sql_agent import get_sql_from_question
from config import DATABASES

app = typer.Typer()

@app.command()
def ask(
    question: str = typer.Option(..., prompt="Câu hỏi dữ liệu bạn muốn truy vấn"),
    db_name: str = typer.Option(..., prompt=f"Tên DB ({', '.join(DATABASES.keys())})")
):
    if db_name not in DATABASES:
        typer.echo(f" DB '{db_name}' chưa được cấu hình.")
        raise typer.Exit()

    uri = DATABASES[db_name]
    typer.echo(f"Đang kết nối đến {db_name}...")

    metadata = asyncio.run(extract_metadata(uri))
    typer.echo(f"Schema:\n{metadata}\n")

    sql = get_sql_from_question(question, metadata)
    typer.echo(f"SQL được sinh:\n{sql}\n")

    rows = asyncio.run(run_query(uri, sql))
    if rows:
        print(tabulate(rows, headers="keys", tablefmt="grid"))
    else:
        print("Không có dữ liệu.")

if __name__ == "__main__":
    app()
