"""Interactive console viewer for PostgreSQL Silver and Gold models."""

from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import text

from sql.connection import db_manager


SILVER_TABLES = {
    "1": ("silver_perfumes_enriched", "Enriched perfumes"),
    "2": ("silver_sales_enriched", "Enriched sales"),
    "3": ("silver_customers_enriched", "Enriched customers"),
    "4": ("silver_inventory_enriched", "Enriched inventory"),
}

GOLD_TABLES = {
    "1": ("gold_revenue_by_brand", "Revenue by brand"),
    "2": ("gold_top_selling_perfumes", "Top-selling perfumes"),
    "3": ("gold_revenue_by_location", "Revenue by location"),
}


def _format_table(headers: Sequence[str], rows: Sequence[Sequence[object]]) -> str:
    """Render a compact table without requiring dataframe libraries."""
    max_width = 32

    def cell(value: object) -> str:
        value = "" if value is None else str(value).replace("\n", " ")
        return value if len(value) <= max_width else value[: max_width - 3] + "..."

    values = [[cell(value) for value in row] for row in rows]
    widths = [len(cell(header)) for header in headers]
    for row in values:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(value))

    separator = "+-" + "-+-".join("-" * width for width in widths) + "-+"
    output = [separator]
    output.append("| " + " | ".join(cell(header).ljust(widths[i]) for i, header in enumerate(headers)) + " |")
    output.append(separator)
    for row in values:
        output.append("| " + " | ".join(value.ljust(widths[i]) for i, value in enumerate(row)) + " |")
    output.append(separator)
    return "\n".join(output)


def show_table(table_name: str, label: str, limit: int = 20) -> None:
    """Display one fixed analytics table, limited to a readable sample."""
    with db_manager.get_engine().connect() as connection:
        result = connection.execute(
            text(f"SELECT * FROM analytics.{table_name} LIMIT :limit"),
            {"limit": limit},
        )
        rows = result.fetchall()
        headers = list(result.keys())

    print(f"\n--- {label} | analytics.{table_name} | {len(rows)} rows shown ---")
    print(_format_table(headers, rows) if rows else "The table has no rows.")


def choose_table(layer: str, tables: dict[str, tuple[str, str]]) -> None:
    while True:
        print(f"\n=== {layer} ===")
        for option, (_, label) in tables.items():
            print(f"{option}) {label}")
        print("0) Back")
        option = input("Choose a table: ").strip()

        if option == "0":
            return
        selected = tables.get(option)
        if selected is None:
            print("Invalid option.")
            continue
        show_table(*selected)
        input("\nPress Enter to continue...")


def main() -> None:
    while True:
        print("\n==============================")
        print("  PERFUMERY - ELT VIEWER")
        print("==============================")
        print("1) View Silver tables")
        print("2) View Gold tables")
        print("0) Exit")
        option = input("Choose an option: ").strip()

        match option:
            case "1":
                choose_table("SILVER", SILVER_TABLES)
            case "2":
                choose_table("GOLD", GOLD_TABLES)
            case "0":
                print("Goodbye.")
                return
            case _:
                print("Invalid option.")


if __name__ == "__main__":
    main()

