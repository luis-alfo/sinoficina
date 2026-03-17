"""
Full setup: provision schema, seed all data, and cleanup default table.
Runs everything in the correct order. Non-fatal — continues on errors.
"""

import sys
import os
import time

# Ensure script directory is in path for local imports
sys.path.insert(0, os.path.dirname(__file__))


def run():
    print("=" * 60)
    print("FULL SETUP - Warner Music Airtable Database")
    print("=" * 60)

    # Step 1: Provision tables
    print("\n[1/6] Provisioning schema...")
    try:
        from provision_schema import provision
        provision()
    except Exception as e:
        print(f"  ERROR: {e}")
    time.sleep(1)

    # Step 2: Cleanup default Table 1
    print("\n[2/6] Cleaning up default table...")
    try:
        from cleanup_default import cleanup
        cleanup()
    except Exception as e:
        print(f"  ERROR: {e}")
    time.sleep(1)

    # Step 3: Seed genres
    print("\n[3/6] Seeding genres...")
    try:
        from seed_data import seed_genres
        seed_genres()
    except Exception as e:
        print(f"  ERROR: {e}")
    time.sleep(1)

    # Step 4: Sync artists
    print("\n[4/6] Syncing Warner artists...")
    try:
        from sync_warner_artists import sync
        sync()
    except Exception as e:
        print(f"  ERROR: {e}")
    time.sleep(1)

    # Step 5: Seed albums
    print("\n[5/6] Seeding albums...")
    try:
        from seed_data import seed_albums
        seed_albums()
    except Exception as e:
        print(f"  ERROR: {e}")
    time.sleep(1)

    # Step 6: Seed songs
    print("\n[6/6] Seeding songs...")
    try:
        from seed_songs import seed
        seed()
    except Exception as e:
        print(f"  ERROR: {e}")

    print("\n" + "=" * 60)
    print("SETUP COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    run()
