import os
import requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


def _get_component(components, component_type):
    for component in components:
        if component_type in component.get("types", []):
            return component.get("long_name", "")
    return ""


def _get_component_short(components, component_type):
    for component in components:
        if component_type in component.get("types", []):
            return component.get("short_name", "")
    return ""


def geocode_address(address: str):
    if not GOOGLE_MAPS_API_KEY:
        return {
            "success": False,
            "error": "Missing GOOGLE_MAPS_API_KEY in .env file.",
            "candidates": [],
        }

    if not address or not address.strip():
        return {
            "success": False,
            "error": "Address is empty.",
            "candidates": [],
        }

    url = "https://maps.googleapis.com/maps/api/geocode/json"

    params = {
        "address": address,
        "components": "country:US",
        "key": GOOGLE_MAPS_API_KEY,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "candidates": [],
        }

    if data.get("status") != "OK":
        return {
            "success": False,
            "error": data.get("status", "Unknown geocoding error"),
            "candidates": [],
        }

    candidates = []

    for result in data.get("results", []):
        components = result.get("address_components", [])
        location = result.get("geometry", {}).get("location", {})

        city = (
            _get_component(components, "locality")
            or _get_component(components, "sublocality")
            or _get_component(components, "administrative_area_level_2")
        )

        state = _get_component_short(components, "administrative_area_level_1")
        zip_code = _get_component(components, "postal_code")

        candidates.append({
            "formatted_address": result.get("formatted_address", ""),
            "city": city,
            "state": state,
            "zip": zip_code,
            "lat": location.get("lat"),
            "lng": location.get("lng"),
        })

    best = candidates[0]

    return {
        "success": True,
        "formatted_address": best["formatted_address"],
        "city": best["city"],
        "state": best["state"],
        "zip": best["zip"],
        "lat": best["lat"],
        "lng": best["lng"],
        "candidates": candidates,
    }