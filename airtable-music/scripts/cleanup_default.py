"""
Delete the default 'Table 1' that Airtable creates automatically.
Run this AFTER provision-schema so the base only has our custom tables.
"""

from airtable_client import find_table_id, delete_table


def cleanup():
    table_id = find_table_id("Table 1")
    if not table_id:
        print("'Table 1' not found — already cleaned up or renamed")
        return

    print(f"Deleting 'Table 1' (ID: {table_id})...")
    result = delete_table(table_id)
    if result is not None:
        print("'Table 1' deleted successfully")
    else:
        print("Failed to delete 'Table 1' — may need at least 2 tables in the base first")


if __name__ == "__main__":
    cleanup()
