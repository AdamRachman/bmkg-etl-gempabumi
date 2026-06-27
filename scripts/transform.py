import pandas as pd


def categorize_severity(magnitude):
    if magnitude < 4:
        return "Lemah"
    elif magnitude < 5:
        return "Ringan"
    elif magnitude < 6:
        return "Sedang"
    else:
        return "Kuat"


def transform_data(raw_data):
    print("[TRANSFORM] Starting transformation...")

    # Step 1: Convert raw list to DataFrame
    df = pd.DataFrame(raw_data)

    # Safety check
    if df.empty:
        raise Exception("[TRANSFORM ERROR] No data received from extract layer.")

    # Step 2: Standardize column names
    df.columns = df.columns.str.lower()

    # Step 3: Rename columns to match canonical schema
    df.rename(columns={
        "coordinates": "koordinat",
        "kedalaman": "kedalaman_km",
    }, inplace=True)

    # Step 4: Ensure required columns exist
    required_columns = [
        "tanggal",
        "jam",
        "datetime_utc",
        "koordinat",
        "lintang",
        "bujur",
        "magnitude",
        "kedalaman_km",
        "wilayah"
    ]

    missing_cols = [col for col in required_columns if col not in df.columns]

    if missing_cols:
        raise Exception(
            f"[TRANSFORM ERROR] Missing required columns: {missing_cols}"
        )

    # Step 5: Convert datetime
    df["datetime_utc"] = pd.to_datetime(
        df["datetime_utc"],
        errors="coerce"
    )

    # Step 6: Convert magnitude to numeric
    df["magnitude"] = pd.to_numeric(
        df["magnitude"],
        errors="coerce"
    )

    # Step 7: Clean kedalaman (remove ' km')
    df["kedalaman_km"] = (
        df["kedalaman_km"]
        .astype(str)
        .str.replace(" km", "", regex=False)
    )

    df["kedalaman_km"] = pd.to_numeric(
        df["kedalaman_km"],
        errors="coerce"
    )

    # Step 8: Add severity category
    df["skala_gempa"] = df["magnitude"].apply(categorize_severity)

    # Step 9: Add source lineage
    # Default current source = gempadirasakan
    # Nanti jika source baru masuk, extractor yang atur value ini
    if "source_data" not in df.columns:
        df["source_data"] = "gempadirasakan"

    # Step 10: Remove exact duplicate rows within batch
    df = df.drop_duplicates(
        subset=["datetime_utc", "koordinat"]
    )

    # Step 11: Final canonical column order
    final_columns = [
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

    df = df[final_columns]

    print(f"[TRANSFORM] Success. Transformed {len(df)} records.")
    print(f"[TRANSFORM] Columns: {list(df.columns)}")

    return df


if __name__ == "__main__":
    from extract import extract_data

    raw_data = extract_data()
    df = transform_data(raw_data)

    print(df.head())
    print(df.dtypes)