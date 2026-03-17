"""
Full setup: provision schema, seed all data, and cleanup default table.
Runs everything in the correct order.
"""

import time


def run():
    print("=" * 60)
    print("FULL SETUP - Warner Music Airtable Database")
    print("=" * 60)

    # Step 1: Provision tables
    print("\n[1/6] Provisioning schema...")
    from provision_schema import provision
    provision()
    time.sleep(1)

    # Step 2: Cleanup default Table 1
    print("\n[2/6] Cleaning up default table...")
    from cleanup_default import cleanup
    cleanup()
    time.sleep(1)

    # Step 3: Seed genres
    print("\n[3/6] Seeding genres...")
    from seed_data import post_records, GENRES
    genres_clean = [{k: v for k, v in g.items() if k != "Género Padre"} for g in GENRES]
    n = post_records("Géneros", genres_clean)
    print(f"  Created {n} genres")
    time.sleep(1)

    # Step 4: Sync artists
    print("\n[4/6] Syncing Warner artists...")
    from sync_warner_artists import create_records, WARNER_ARTISTS
    create_records(WARNER_ARTISTS)
    time.sleep(1)

    # Step 5: Seed albums
    print("\n[5/6] Seeding albums...")
    from seed_data import SAMPLE_ALBUMS
    n = post_records("Álbumes", SAMPLE_ALBUMS)
    print(f"  Created {n} albums")
    time.sleep(1)

    # Step 6: Seed songs
    print("\n[6/6] Seeding songs...")
    from seed_songs import SAMPLE_SONGS
    from airtable_client import create_records as cr
    n = cr("Canciones", SAMPLE_SONGS)
    print(f"  Created {n} songs")

    print("\n" + "=" * 60)
    print("SETUP COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    run()
