from scripts.extract import extract_data
from scripts.transform import transform_data
from scripts.load_bigquery import load_data_bigquery


def main_bigquery():
    print("========== BMKG BIGQUERY ETL START ==========")

    # =========================
    # EXTRACT (MULTI SOURCE)
    # =========================
    try:
        all_raw_data = []

        # Source 1: gempadirasakan
        print("[EXTRACT] Starting extraction from gempadirasakan...")
        raw_gd = extract_data("gempadirasakan")

        if raw_gd:
            print(f"[EXTRACT] gempadirasakan success: {len(raw_gd)} records.")
            all_raw_data.extend(raw_gd)
        else:
            print("[EXTRACT WARNING] No data from gempadirasakan.")

        # Source 2: gempaterkini
        print("[EXTRACT] Starting extraction from gempaterkini...")
        raw_gt = extract_data("gempaterkini")

        if raw_gt:
            print(f"[EXTRACT] gempaterkini success: {len(raw_gt)} records.")
            all_raw_data.extend(raw_gt)
        else:
            print("[EXTRACT WARNING] No data from gempaterkini.")

        if not all_raw_data:
            raise Exception("No data extracted from all BMKG sources.")

        print(f"[EXTRACT] Total combined records: {len(all_raw_data)}")

    except Exception as e:
        print(f"[EXTRACT ERROR] {str(e)}")
        raise

    # =========================
    # TRANSFORM
    # =========================
    try:
        print("[TRANSFORM] Starting transformation...")
        df = transform_data(all_raw_data)

        if df.empty:
            raise Exception("Transformation produced empty DataFrame.")

        print(f"[TRANSFORM] Success. Transformed {len(df)} records.")
        print(f"[TRANSFORM] Columns: {df.columns.tolist()}")

        if "source_data" in df.columns:
            print("[TRANSFORM] Source distribution:")
            print(df["source_data"].value_counts())

    except Exception as e:
        print(f"[TRANSFORM ERROR] {str(e)}")
        raise

    # =========================
    # LOAD TO BIGQUERY
    # =========================
    try:
        print("[LOAD] Starting BigQuery load process...")
        load_data_bigquery(df)

        print("[LOAD] Success. Data loaded to BigQuery.")

    except Exception as e:
        print(f"[LOAD ERROR] {str(e)}")
        raise

    print("========== BMKG BIGQUERY ETL COMPLETE ==========")


if __name__ == "__main__":
    main_bigquery()