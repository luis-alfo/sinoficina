"""
Shared Airtable API client used by all scripts.
"""

import json
import os
import sys
import time
from urllib.parse import quote
from urllib.request import Request, urlopen
from urllib.error import HTTPError

BASE_ID = os.environ.get("AIRTABLE_BASE_ID", "appGiSPPxrhb0LXYe")
API_KEY = os.environ.get("AIRTABLE_API_KEY", "")

API_BASE = f"https://api.airtable.com/v0/{BASE_ID}"
META_BASE = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}"


def table_url(table_name):
    """Build a properly encoded URL for a table."""
    return f"{API_BASE}/{quote(table_name, safe='')}"


def api_request(url, data=None, method="GET"):
    """Make an authenticated request to the Airtable API."""
    if not API_KEY:
        raise RuntimeError("AIRTABLE_API_KEY environment variable not set")

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
        raise


def list_records(table_name, fields=None, max_records=100, view=None):
    """List records from a table."""
    base = table_url(table_name)
    params = [f"maxRecords={max_records}"]
    if fields:
        for f in fields:
            params.append(f"fields[]={quote(f, safe='')}")
    if view:
        params.append(f"view={quote(view, safe='')}")
    url = base + "?" + "&".join(params) if params else base

    all_records = []
    while url:
        result = api_request(url)
        all_records.extend(result.get("records", []))
        offset = result.get("offset")
        url = f"{base}?offset={offset}&maxRecords={max_records}" if offset else None

    return all_records


def create_records(table_name, records_data):
    """Create records in a table. Handles batching (max 10 per request)."""
    url = table_url(table_name)
    created = 0
    errors = []

    for i in range(0, len(records_data), 10):
        batch = records_data[i:i + 10]
        records = [{"fields": item} for item in batch]
        try:
            result = api_request(url, data={"records": records}, method="POST")
            created += len(result.get("records", []))
        except Exception as e:
            errors.append(str(e))
        time.sleep(0.25)

    if created == 0 and records_data:
        raise RuntimeError(
            f"Failed to create any records in '{table_name}'. Errors: {'; '.join(errors)}"
        )

    return created


def update_records(table_name, records):
    """Update records. Each item needs 'id' and 'fields'."""
    url = table_url(table_name)
    updated = 0

    for i in range(0, len(records), 10):
        batch = records[i:i + 10]
        result = api_request(url, data={"records": batch}, method="PATCH")
        updated += len(result.get("records", []))
        time.sleep(0.25)

    return updated


def delete_records(table_name, record_ids):
    """Delete records by ID. Max 10 per request."""
    deleted = 0
    base = table_url(table_name)
    for i in range(0, len(record_ids), 10):
        batch = record_ids[i:i + 10]
        params = "&".join(f"records[]={rid}" for rid in batch)
        url = f"{base}?{params}"
        result = api_request(url, method="DELETE")
        deleted += len(result.get("records", []))
        time.sleep(0.25)

    return deleted


def get_tables():
    """Get all tables in the base."""
    result = api_request(f"{META_BASE}/tables")
    if not result:
        return []
    return result.get("tables", [])


def find_table_id(table_name):
    """Find table ID by name."""
    for t in get_tables():
        if t["name"] == table_name:
            return t["id"]
    return None


def delete_table(table_id):
    """Delete a table by ID."""
    url = f"{META_BASE}/tables/{table_id}"
    return api_request(url, method="DELETE")
