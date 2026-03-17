"""
Fetch the current schema of the Airtable base and save it locally.
Uses the Airtable Metadata API to retrieve table and field definitions.
"""

import json
import os
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError

BASE_ID = os.environ.get("AIRTABLE_BASE_ID", "appGiSPPxrhb0LXYe")
API_KEY = os.environ.get("AIRTABLE_API_KEY", "")

METADATA_URL = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables"

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "schemas")


def fetch_schema():
    if not API_KEY:
        print("Error: AIRTABLE_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    req = Request(METADATA_URL, headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    })

    try:
        with urlopen(req) as resp:
            data = json.loads(resp.read().decode())
    except HTTPError as e:
        print(f"Error fetching schema: {e.code} {e.reason}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, "airtable_current_schema.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Schema saved to {output_path}")
    print(f"Found {len(data.get('tables', []))} tables:")
    for table in data.get("tables", []):
        fields = table.get("fields", [])
        print(f"  - {table['name']}: {len(fields)} fields")

    return data


if __name__ == "__main__":
    fetch_schema()
