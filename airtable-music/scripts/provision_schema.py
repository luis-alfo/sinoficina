"""
Provision tables and fields in Airtable based on the local schema definition.
Uses the Airtable Metadata API to CREATE tables with their fields.
"""

import json
import os
import time
from airtable_client import api_request, get_tables, META_BASE

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "..", "schemas", "music_database.json")
TABLES_URL = f"{META_BASE}/tables"

SKIP_TYPES = {"count"}
LINKED_TYPE = "multipleRecordLinks"

# Types the Airtable API doesn't support for creation — use singleLineText as fallback
UNSUPPORTED_CREATE_TYPES = {"aiText"}


def get_existing_tables():
    tables = get_tables()
    return {t["name"]: t for t in tables}


def get_existing_field_names(table_info):
    return {f["name"] for f in table_info.get("fields", [])}


def build_field_config(name, field_def):
    field_type = field_def["type"]

    if field_type in UNSUPPORTED_CREATE_TYPES:
        return None

    config = {"name": name, "type": field_type}

    if "description" in field_def:
        config["description"] = field_def["description"]

    if field_type in ("singleSelect", "multipleSelects") and "options" in field_def:
        colors = [
            "blueLight2", "cyanLight2", "tealLight2", "greenLight2",
            "yellowLight2", "orangeLight2", "redLight2", "pinkLight2",
            "purpleLight2", "grayLight2",
        ]
        choices = [{"name": opt, "color": colors[i % len(colors)]} for i, opt in enumerate(field_def["options"])]
        config["options"] = {"choices": choices}

    if field_type == "number":
        config["options"] = {"precision": 0 if field_def.get("format") == "integer" else 1}

    if field_type == "rating":
        config["options"] = {"max": field_def.get("max", 5), "color": "yellowBright"}

    if field_type == "currency":
        config["options"] = {"precision": 2, "symbol": field_def.get("symbol", "$")}

    if field_type == "duration":
        config["options"] = {"durationFormat": "h:mm:ss"}

    if field_type == "date":
        config["options"] = {"dateFormat": {"name": "iso"}}

    if field_type == "percent":
        config["options"] = {"precision": 2}

    if field_type == "checkbox":
        config["options"] = {"icon": "check", "color": "greenBright"}

    return config


def add_missing_fields(table_name, table_def, existing_tables, table_id_map):
    """Add fields defined in schema but missing from the existing Airtable table."""
    table_info = existing_tables.get(table_name)
    if not table_info:
        return

    table_id = table_info["id"]
    existing_fields = get_existing_field_names(table_info)
    fields_url = f"{TABLES_URL}/{table_id}/fields"

    for field_name, field_def in table_def["fields"].items():
        if field_name in existing_fields:
            continue
        if field_def["type"] == LINKED_TYPE or field_def["type"] in SKIP_TYPES:
            continue

        config = build_field_config(field_name, field_def)
        if not config:
            continue

        print(f"  Adding field '{field_name}' to '{table_name}'...")
        try:
            result = api_request(fields_url, data=config, method="POST")
            if "id" in result:
                print(f"  [ok] {field_name} -> {result['id']}")
            else:
                print(f"  [FAIL] {field_name}")
        except Exception as e:
            print(f"  [FAIL] {field_name}: {e}")
        time.sleep(0.3)


def create_table(table_name, table_def, existing_tables, table_id_map):
    if table_name in existing_tables:
        print(f"  [exists] '{table_name}' — checking for missing fields...")
        table_id_map[table_name] = existing_tables[table_name]["id"]
        add_missing_fields(table_name, table_def, existing_tables, table_id_map)
        return

    fields = []
    for field_name, field_def in table_def["fields"].items():
        if field_def["type"] == LINKED_TYPE or field_def["type"] in SKIP_TYPES:
            continue
        config = build_field_config(field_name, field_def)
        if config:
            fields.append(config)

    if not fields:
        fields.append({"name": "Name", "type": "singleLineText"})

    # Airtable requires the first field (primary) to be singleLineText
    # Move the first singleLineText to position 0 if it's not already there
    if fields[0]["type"] != "singleLineText":
        for i, f in enumerate(fields):
            if f["type"] == "singleLineText":
                fields.insert(0, fields.pop(i))
                break
        else:
            # No singleLineText found, insert one
            fields.insert(0, {"name": "Nombre", "type": "singleLineText"})

    payload = {"name": table_name, "fields": fields}
    if "description" in table_def:
        payload["description"] = table_def["description"]

    print(f"  Creating '{table_name}' ({len(fields)} fields)...")
    result = api_request(TABLES_URL, data=payload, method="POST")
    if "id" in result:
        table_id_map[table_name] = result["id"]
        print(f"  [ok] '{table_name}' -> {result['id']}")
    else:
        raise RuntimeError(f"Could not create table '{table_name}': unexpected response")


def add_linked_fields(table_name, table_def, table_id_map, existing_tables):
    table_id = table_id_map.get(table_name)
    if not table_id:
        return

    existing_fields = get_existing_field_names(existing_tables.get(table_name, {}))
    fields_url = f"{TABLES_URL}/{table_id}/fields"

    for field_name, field_def in table_def["fields"].items():
        if field_def["type"] != LINKED_TYPE:
            continue

        if field_name in existing_fields:
            print(f"  [skip] {table_name}.{field_name} already exists")
            continue

        linked_table = field_def["linkedTable"]
        linked_table_id = table_id_map.get(linked_table)
        if not linked_table_id:
            print(f"  [skip] {table_name}.{field_name} -> '{linked_table}' not found")
            continue

        config = {
            "name": field_name,
            "type": "multipleRecordLinks",
            "options": {"linkedTableId": linked_table_id},
        }

        print(f"  Linking {table_name}.{field_name} -> {linked_table}")
        try:
            result = api_request(fields_url, data=config, method="POST")
            if "id" in result:
                print(f"  [ok] {field_name}")
            else:
                print(f"  [FAIL] {field_name}")
        except Exception as e:
            print(f"  [FAIL] {field_name}: {e}")
        time.sleep(0.3)


def provision():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = json.load(f)

    tables = schema["tables"]
    existing = get_existing_tables()
    table_id_map = {}

    print(f"Existing tables: {len(existing)} | Schema defines: {len(tables)}\n")

    print("=== Pass 1: Create tables ===")
    for table_name, table_def in tables.items():
        create_table(table_name, table_def, existing, table_id_map)
        time.sleep(0.3)

    # Refresh existing tables for pass 2 (to check existing fields)
    existing = get_existing_tables()

    print("\n=== Pass 2: Link fields ===")
    for table_name, table_def in tables.items():
        add_linked_fields(table_name, table_def, table_id_map, existing)

    print(f"\nDone! {len(table_id_map)} tables provisioned.")


if __name__ == "__main__":
    provision()
