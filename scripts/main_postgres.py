from scripts.extract import extract_data
from scripts.transform import transform_data
from scripts.load import load_data


def main():
    print("========== STARTING ETL PROCESS ==========")

    # =========================
    # EXTRACT (MULTI SOURCE)
    # =========================
    try:
        print("[EXTRACT] Starting extraction from gempadirasakan...")
        raw_dirasakan = extract_data("gempadirasakan")
        print(f"[EXTRACT] gempadirasakan success: {len(raw_dirasakan)} records.")

        print("[EXTRACT] Starting extraction from gempaterkini...")
        raw_terkini = extract_data("gempaterkini")
        print(f"[EXTRACT] gempaterkini success: {len(raw_terkini)} records.")

        # Combine both sources
        raw_data = raw_dirasakan + raw_terkini

        if not raw_data:
            raise Exception("No data extracted from any source.")

        print(f"[EXTRACT] Total combined records: {len(raw_data)}")

    except Exception as e:
        print(f"[EXTRACT ERROR] {str(e)}")
        raise

    # =========================
    # TRANSFORM
    # =========================
    try:
        print("[TRANSFORM] Starting transformation...")
        df = transform_data(raw_data)

        if df.empty:
            raise Exception("Transformation produced empty DataFrame.")

        print(f"[TRANSFORM] Success. Transformed {len(df)} records.")
        print(f"[TRANSFORM] Columns: {df.columns.tolist()}")

        # Optional visibility for source distribution
        if "source_data" in df.columns:
            print("[TRANSFORM] Source distribution:")
            print(df["source_data"].value_counts())

    except Exception as e:
        print(f"[TRANSFORM ERROR] {str(e)}")
        raise

    # =========================
    # LOAD
    # =========================
    try:
        print("[LOAD] Starting load process...")
        load_data(df)

        print("[LOAD] Success. Data loaded to PostgreSQL.")

    except Exception as e:
        print(f"[LOAD ERROR] {str(e)}")
        raise

    print("========== ETL PROCESS COMPLETED ==========")


if __name__ == "__main__":
    main()