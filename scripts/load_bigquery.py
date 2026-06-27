import os
import pandas as pd
from google.cloud import bigquery

# =========================================================
# GCP CONFIG
# =========================================================
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/mnt/c/airflow/keys/bmkg-key.json"

PROJECT_ID = "bmkg-earthquake-etl"
DATASET_ID = "earthquake_dataset"
TABLE_ID = "earthquakes"


# =========================================================
# BIGQUERY LOAD FUNCTION
# =========================================================
def load_data_bigquery(df):
    print("[LOAD] Starting BigQuery load...")

    client = bigquery.Client(project=PROJECT_ID)

    # =====================================================
    # STEP 0: Normalize incoming dataframe
    # Keep datetime_utc as TIMESTAMP for BigQuery
    # Add datetime_key ONLY for dedup consistency
    # =====================================================
    df["datetime_utc"] = pd.to_datetime(
        df["datetime_utc"],
        errors="coerce",
        utc=True
    )

    df = df.dropna(subset=["datetime_utc", "koordinat"])

    df["datetime_key"] = df["datetime_utc"].dt.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # =====================================================
    # STEP 1: Get existing keys from BigQuery
    # =====================================================
    query = f"""
    SELECT datetime_utc, koordinat
    FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
    """

    existing_df = client.query(query).to_dataframe(
        create_bqstorage_client=False
    )

    # If table already has data
    if not existing_df.empty:
        existing_df["datetime_utc"] = pd.to_datetime(
            existing_df["datetime_utc"],
            errors="coerce",
            utc=True
        )

        existing_df = existing_df.dropna(
            subset=["datetime_utc", "koordinat"]
        )

        existing_df["datetime_key"] = existing_df[
            "datetime_utc"
        ].dt.strftime("%Y-%m-%d %H:%M:%S")

        existing_keys = {
            (row["datetime_key"], row["koordinat"])
            for _, row in existing_df.iterrows()
        }

    else:
        existing_keys = set()

    print(f"[LOAD] Existing rows before load: {len(existing_df)}")

    # =====================================================
    # STEP 2: Dedup logic
    # Compare normalized datetime_key + koordinat
    # =====================================================
    new_data = df[
        ~df.apply(
            lambda row: (
                row["datetime_key"],
                row["koordinat"]
            ) in existing_keys,
            axis=1
        )
    ].copy()

    print(f"[LOAD] New unique rows: {len(new_data)}")

    # =====================================================
    # STEP 3: Stop if no new rows
    # =====================================================
    if new_data.empty:
        print("[LOAD] No new data to upload.")
        return

    # =====================================================
    # STEP 4: Drop helper column before upload
    # BigQuery schema does NOT need datetime_key
    # =====================================================
    new_data.drop(columns=["datetime_key"], inplace=True)

    # =====================================================
    # STEP 5: Upload to BigQuery
    # =====================================================
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_APPEND"
    )

    job = client.load_table_from_dataframe(
        new_data,
        table_ref,
        job_config=job_config
    )

    job.result()

    print(f"[LOAD] Success. {len(new_data)} rows uploaded.")

    # =====================================================
    # STEP 6: Final Validation
    # =====================================================
    count_query = f"""
    SELECT COUNT(*) AS total_rows
    FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
    """

    total_rows = client.query(count_query).to_dataframe(
        create_bqstorage_client=False
    )["total_rows"][0]

    print(f"[VALIDATION] Final total rows in BigQuery: {total_rows}")