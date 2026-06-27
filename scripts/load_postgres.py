from sqlalchemy import create_engine, text
from psycopg2.extras import execute_values


DB_URL = "postgresql+psycopg2://de_user:adam@localhost:5432/earthquake_db"


def load_data(df):
    print("[LOAD] Starting load process...")

    # Step 1: Create engine
    engine = create_engine(DB_URL)

    # Safety check
    if df.empty:
        raise Exception("[LOAD ERROR] DataFrame is empty. Nothing to load.")

    # Step 2: Get existing unique keys from database
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT datetime_utc, koordinat FROM earthquakes")
            )

            existing_keys = {
                (row[0], row[1]) for row in result.fetchall()
            }

    except Exception as e:
        print(f"[LOAD ERROR] Failed reading existing data: {e}")
        raise

    # Step 3: Filter only new records
    new_data = df[
        ~df.apply(
            lambda row: (
                row["datetime_utc"],
                row["koordinat"]
            ) in existing_keys,
            axis=1
        )
    ]

    print(f"[LOAD] Incoming rows: {len(df)}")
    print(f"[LOAD] New rows after dedup: {len(new_data)}")

    if new_data.empty:
        print("[LOAD] No new data to load. All records already exist.")
        return

    # Step 4: Canonical insert columns
    insert_columns = [
        "tanggal",
        "jam",
        "datetime_utc",
        "koordinat",
        "lintang",
        "bujur",
        "magnitude",
        "kedalaman_km",
        "wilayah",
        "skala_gempa",
        "source_data"
    ]

    # Safety check for schema mismatch
    missing_cols = [col for col in insert_columns if col not in new_data.columns]

    if missing_cols:
        raise Exception(
            f"[LOAD ERROR] Missing required columns for insert: {missing_cols}"
        )

    # Step 5: Prepare records for bulk insert
    records = [
        tuple(row[col] for col in insert_columns)
        for _, row in new_data.iterrows()
    ]

    # Step 6: Insert query
    insert_query = """
        INSERT INTO earthquakes (
            tanggal,
            jam,
            datetime_utc,
            koordinat,
            lintang,
            bujur,
            magnitude,
            kedalaman_km,
            wilayah,
            skala_gempa,
            source_data
        ) VALUES %s
    """

    # Step 7: Bulk insert using psycopg2
    raw_conn = engine.raw_connection()

    try:
        with raw_conn.cursor() as cur:
            execute_values(cur, insert_query, records)

        raw_conn.commit()

    except Exception as e:
        raw_conn.rollback()
        print(f"[LOAD ERROR] Insert failed: {e}")
        raise

    finally:
        raw_conn.close()

    print(f"[LOAD] Success. {len(new_data)} new records loaded successfully.")