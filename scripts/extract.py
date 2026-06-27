import cloudscraper
import xml.etree.ElementTree as ET


SOURCE_URLS = {
    "gempadirasakan": "https://data.bmkg.go.id/DataMKG/TEWS/gempadirasakan.xml",
    "gempaterkini": "https://data.bmkg.go.id/DataMKG/TEWS/gempaterkini.xml"
}


def extract_data(source_type="gempadirasakan"):
    print(f"[EXTRACT] Starting extraction from {source_type}...")

    if source_type not in SOURCE_URLS:
        raise Exception(f"[EXTRACT ERROR] Unknown source_type: {source_type}")

    url = SOURCE_URLS[source_type]

    scraper = cloudscraper.create_scraper(
        browser={
            "browser": "chrome",
            "platform": "windows",
            "mobile": False
        }
    )

    response = scraper.get(url, timeout=30)

    if response.status_code != 200:
        raise Exception(
            f"[EXTRACT ERROR] Failed with status code: {response.status_code}"
        )

    xml_data = response.text

    if "Akses diblokir" in xml_data:
        raise Exception(
            "[EXTRACT ERROR] BMKG blocked access."
        )

    root = ET.fromstring(xml_data)

    gempa_list = []

    for gempa in root.findall("gempa"):
        gempa_list.append({
            "tanggal": gempa.findtext("Tanggal"),
            "jam": gempa.findtext("Jam"),
            "datetime_utc": gempa.findtext("DateTime"),
            "coordinates": gempa.findtext("point/coordinates"),
            "lintang": gempa.findtext("Lintang"),
            "bujur": gempa.findtext("Bujur"),
            "magnitude": gempa.findtext("Magnitude"),
            "kedalaman": gempa.findtext("Kedalaman"),
            "wilayah": gempa.findtext("Wilayah"),
            "source_data": source_type
        })

    if not gempa_list:
        raise Exception("[EXTRACT ERROR] No data found.")

    print(
        f"[EXTRACT] Success. Extracted {len(gempa_list)} records from {source_type}."
    )

    return gempa_list