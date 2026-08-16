import os
import requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


def get_streetview_url(lat, lng, width=640, height=420):
    if not GOOGLE_MAPS_API_KEY:
        return None

    metadata_url = "https://maps.googleapis.com/maps/api/streetview/metadata"

    metadata_params = {
        "location": f"{lat},{lng}",
        "key": GOOGLE_MAPS_API_KEY,
    }

    try:
        metadata_response = requests.get(metadata_url, params=metadata_params, timeout=10)
        metadata = metadata_response.json()
    except Exception:
        return None

    if metadata.get("status") != "OK":
        return None

    image_url = (
        "https://maps.googleapis.com/maps/api/streetview"
        f"?size={width}x{height}"
        f"&location={lat},{lng}"
        f"&fov=80"
        f"&pitch=0"
        f"&key={GOOGLE_MAPS_API_KEY}"
    )

    return image_url