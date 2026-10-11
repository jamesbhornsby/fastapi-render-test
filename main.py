
import csv
from pathlib import Path

from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import FileResponse

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
HTML_FILE = BASE_DIR / "static" / "hack.html"
DATA_FILE = BASE_DIR / "data" / "readings.csv"


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(HTML_FILE)


@app.get("/api/readings")
def get_readings(
    workedId: str = Query(...),
    deviceId: str = Query(...),
):
    if not DATA_FILE.exists():
        raise HTTPException(
            status_code=500,
            detail="Dataset file was not found."
        )

    results = []

    with DATA_FILE.open(
        "r", newline="", encoding="utf-8-sig"
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Support either spelling in the source dataset.
            worker = (
                row.get("workedId")
                or row.get("workerId")
                or ""
            ).strip()

            device = (row.get("deviceId") or "").strip()

            # Only return the selected worker and device.
            if worker != workedId or device != deviceId:
                continue

            try:
                temperature = float(row["temperatureC"])
                air_signal = float(row["airSignalRaw"])
            except (KeyError, TypeError, ValueError):
                # Ignore records with missing or invalid measurements.
                continue

            results.append({
                # These response keys match the original JavaScript.
                "workedId": worker,
                "deviceId": device,
                "temperatureC": temperature,
                "airSignalRaw": air_signal,
                "time": (row.get("time") or "").strip(),
            })

    return results[-500:]