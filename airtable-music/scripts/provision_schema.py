"""
Provision tables and fields in Airtable based on the local schema definition.
Uses the Airtable Metadata API to CREATE tables with their fields.

This script reads music_database.json and creates the tables in the Airtable base.
It handles field types, select options, and linked record relationships.

Usage:
    export AIRTABLE_API_KEY="your_token"
    python scripts/provision_schema.py
"""

import json
import os
import sys
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError

BASE_ID = os.environ.get("AIRTABLE_BASE_ID", "appGiSPPxrhb0LXYe")
API_KEY = os.environ.get("AIRTABLE_API_KEY", "")

TABLES_URL = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables"
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "..", "schemas", "music_database.json")

# Types that need special API formatting
SKIP_TYPES = {"count"}  # count fields are auto-created with linked records
LINKED_TYPE = "multipleRecordLinks"


def api_request(url, data=None, method="GET"):
    """Make an authenticated request to the Airtable API."""
    if not API_KEY:
        print("Error: AIRTABLE_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    body = json.dumps(data).encode() if data else None
    req = Request(url, data=body, method=method, headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    })

    try:
        with urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        print(f"API Error: {e.code} {e.reason}\n{error_body}", file=sys.stderr)
        return None


def get_existing_tables():
    """Fetch current tables in the base."""
    result = api_request(TABLES_URL)
    if not result:
        return {}
    return {t["name"]: t["id"] for t in result.get("tables", [])}


def build_field_config(name, field_def):
    """Convert our schema field definition to Airtable API format."""
    field_type = field_def["type"]

    config = {"name": name, "type": field_type}

    if "description" in field_def:
        config["description"] = field_def["description"]

    # singleSelect / multipleSelects options
    if field_type in ("singleSelect", "multipleSelects") and "options" in field_def:
        colors = [
            "blueLight2", "cyanLight2", "tealLight2", "greenLight2",
            "yellowLight2", "orangeLight2", "redLight2", "pinkLight2",
            "purpleLight2", "grayLight2",
        ]
        choices = []
        for i, opt in enumerate(field_def["options"]):
            choices.append({"name": opt, "color": colors[i % len(colors)]})
        config["options"] = {"choices": choices}

    # number format
    if field_type == "number" and field_def.get("format") == "integer":
        config["options"] = {"precision": 0}

    # rating
    if field_type == "rating":
        config["options"] = {"max": field_def.get("max", 5), "color": "yellowBright"}

    # currency
    if field_type == "currency":
        config["options"] = {"precision": 2, "symbol": field_def.get("symbol", "$")}

    # duration
    if field_type == "duration":
        config["options"] = {"durationFormat": "h:mm:ss"}

    # date
    if field_type == "date":
        config["options"] = {"dateFormat": {"name": "iso"}}

    # percent
    if field_type == "percent":
        config["options"] = {"precision": 2}

    return config


def create_table(table_name, table_def, existing_tables, table_id_map):
    """Create a single table with its non-linked fields."""
    if table_name in existing_tables:
        print(f"  Table '{table_name}' already exists, skipping creation")
        table_id_map[table_name] = existing_tables[table_name]
        return existing_tables[table_name]

    fields = []
    for field_name, field_def in table_def["fields"].items():
        field_type = field_def["type"]

        # Skip linked records (created in second pass) and count fields
        if field_type == LINKED_TYPE or field_type in SKIP_TYPES:
            continue

        config = build_field_config(field_name, field_def)
        fields.append(config)

    # Airtable requires at least one field; the first singleLineText becomes primary
    if not fields:
        fields.append({"name": "Name", "type": "singleLineText"})

    payload = {
        "name": table_name,
        "fields": fields,
    }
    if "description" in table_def:
        payload["description"] = table_def["description"]

    print(f"  Creating table '{table_name}' with {len(fields)} fields...")
    result = api_request(TABLES_URL, data=payload, method="POST")
    if result:
        table_id = result["id"]
        table_id_map[table_name] = table_id
        print(f"  Created '{table_name}' (ID: {table_id})")
        return table_id
    return None


def add_linked_fields(table_name, table_def, table_id_map):
    """Add linked record fields to an existing table (second pass)."""
    table_id = table_id_map.get(table_name)
    if not table_id:
        print(f"  Cannot add links to '{table_name}': table ID not found")
        return

    url = f"{TABLES_URL}/{table_id}/fields"

    for field_name, field_def in table_def["fields"].items():
        if field_def["type"] != LINKED_TYPE:
            continue

        linked_table = field_def["linkedTable"]
        linked_table_id = table_id_map.get(linked_table)
        if not linked_table_id:
            print(f"  Cannot link '{field_name}' -> '{linked_table}': target table not found")
            continue

        # Self-linking (e.g., Géneros -> Género Padre)
        config = {
            "name": field_name,
            "type": "multipleRecordLinks",
            "options": {
                "linkedTableId": linked_table_id,
            },
        }

        print(f"  Adding link: {table_name}.{field_name} -> {linked_table}")
        result = api_request(url, data=config, method="POST")
        if result:
            print(f"    Created field '{field_name}'")
        # Rate limit: Airtable allows 5 requests/second
        time.sleep(0.25)


def provision():
    """Main provisioning logic."""
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = json.load(f)

    tables = schema["tables"]
    existing = get_existing_tables()
    table_id_map = {}

    print(f"Found {len(existing)} existing tables in base")
    print(f"Schema defines {len(tables)} tables\n")

    # Pass 1: Create all tables with non-linked fields
    print("=== Pass 1: Creating tables ===")
    for table_name, table_def in tables.items():
        create_table(table_name, table_def, existing, table_id_map)
        time.sleep(0.25)

    # Pass 2: Add linked record fields
    print("\n=== Pass 2: Adding linked record fields ===")
    for table_name, table_def in tables.items():
        add_linked_fields(table_name, table_def, table_id_map)

    print(f"\nProvisioning complete! {len(table_id_map)} tables ready.")
    print("Table IDs:")
    for name, tid in table_id_map.items():
        print(f"  {name}: {tid}")


if __name__ == "__main__":
    provision()
