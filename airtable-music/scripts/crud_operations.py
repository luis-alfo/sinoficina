"""
Generic CRUD operations for any table. Accepts JSON input via CLI arguments.

Usage:
    # Add artist
    python crud_operations.py add Artistas '{"Nombre": "Bad Bunny", "País": "Puerto Rico"}'

    # Add album
    python crud_operations.py add Álbumes '{"Título": "Un Verano Sin Ti", "Tipo": "Álbum"}'

    # Add songs (array)
    python crud_operations.py add Canciones '[{"Título": "Song 1"}, {"Título": "Song 2"}]'

    # List records
    python crud_operations.py list Artistas

    # List with specific fields
    python crud_operations.py list Artistas '["Nombre", "País", "Sello"]'

    # Delete records
    python crud_operations.py delete Artistas '["recXXX", "recYYY"]'
"""

import json
import sys
from airtable_client import create_records, list_records, delete_records


def cmd_add(table, data_json):
    data = json.loads(data_json)
    if isinstance(data, dict):
        data = [data]
    n = create_records(table, data)
    print(f"Created {n} record(s) in {table}")


def cmd_list(table, fields_json=None):
    fields = json.loads(fields_json) if fields_json else None
    records = list_records(table, fields=fields)
    print(f"\n{table} ({len(records)} records):")
    print("-" * 60)
    for r in records:
        rid = r["id"]
        f = r["fields"]
        # Show first text field as label
        label = next((v for v in f.values() if isinstance(v, str)), rid)
        print(f"  [{rid}] {label}")
        for k, v in f.items():
            if isinstance(v, str) and v == label:
                continue
            print(f"      {k}: {v}")
        print()


def cmd_delete(table, ids_json):
    ids = json.loads(ids_json)
    n = delete_records(table, ids)
    print(f"Deleted {n} record(s) from {table}")


def main():
    if len(sys.argv) < 3:
        print("Usage: python crud_operations.py <add|list|delete> <table> [json_data]")
        sys.exit(1)

    action = sys.argv[1]
    table = sys.argv[2]
    data = sys.argv[3] if len(sys.argv) > 3 else None

    if action == "add":
        if not data:
            print("Error: JSON data required for add", file=sys.stderr)
            sys.exit(1)
        cmd_add(table, data)
    elif action == "list":
        cmd_list(table, data)
    elif action == "delete":
        if not data:
            print("Error: Record IDs required for delete", file=sys.stderr)
            sys.exit(1)
        cmd_delete(table, data)
    else:
        print(f"Unknown action: {action}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
