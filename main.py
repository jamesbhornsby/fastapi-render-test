
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Live Clock</title>
    </head>
    <body>
        <h1>Current Time</h1>
        <p id="time">Loading...</p>

        <script>
            async function updateTime() {
                try {
                    const response = await fetch("/api/time");

                    if (!response.ok) {
                        throw new Error("Request failed");
                    }

                    const data = await response.json();

                    document.getElementById("time").textContent =
                        new Date(data.utc_time).toLocaleTimeString();

                } catch (error) {
                    document.getElementById("time").textContent =
                        "Unable to retrieve time";
                }
            }

            updateTime();
            setInterval(updateTime, 1000);
        </script>
    </body>
    </html>
    """


@app.get("/api/time")
async def get_time():
    current_time = datetime.now(timezone.utc)

    return {
        "utc_time": current_time.isoformat()
    }