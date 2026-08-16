import os
import re
import requests
import tempfile
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from dotenv import load_dotenv
from fpdf import FPDF

load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

st.set_page_config(
    page_title="HazardShield AI",
    page_icon="🛡️",
    layout="wide"
)

TEST_ADDRESSES = [
    "3213 W Barcelona St, Tampa, FL, 33629",
    "1265 N Harvard Blvd, Los Angeles, CA 90029",
    "2621 W Windsor Ave, Chicago, IL 60625",
    "428 Whittier St NW, Washington, DC 20012",
    "14403 Tivoli Dr, Houston, TX 77077",
    "1542 Vrain Street, Denver, CO 80204",
    "4400 Bellwood Ln, Charlotte, NC 28270",
    "203 Tesoro Terrace, St. Augustine, FL 32095",
    "3821 Cogburn Rd, Bismarck, ND 58503",
    "120 Maxwell Xing, Brentwood, TN 37027",
    "3115 E Jefferson St, Seattle, WA 98122",
]

STATE_NAMES = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware",
    "DC": "District of Columbia", "FL": "Florida", "GA": "Georgia", "HI": "Hawaii",
    "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa",
    "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine",
    "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota",
    "MS": "Mississippi", "MO": "Missouri", "MT": "Montana", "NE": "Nebraska",
    "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico",
    "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio",
    "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island",
    "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas",
    "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington",
    "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming",
}

HAZARD_LABELS = {
    "hurricane_wind": "Hurricane / Strong Wind",
    "flood": "Flooding / Heavy Rain",
    "storm_surge": "Storm Surge / Coastal Flooding",
    "extreme_heat": "Extreme Heat",
    "earthquake": "Earthquake",
    "wildfire": "Wildfire / Smoke",
    "hail": "Hail",
    "winter_weather": "Winter Weather / Freeze",
    "tornado": "Tornado",
    "urban_flooding": "Urban Flooding",
    "landslide": "Landslide",
}

HAZARD_DESCRIPTIONS = {
    "hurricane_wind": "Wind damage from hurricanes, tropical storms, or severe wind events.",
    "flood": "Water damage from heavy rainfall, poor drainage, rivers, or localized flooding.",
    "storm_surge": "Coastal flooding caused by storm-driven water pushed inland.",
    "extreme_heat": "High-temperature exposure affecting comfort, health, and energy resilience.",
    "earthquake": "Ground shaking risk that can damage foundations, walls, and utilities.",
    "wildfire": "Risk from wildfire exposure, embers, smoke, or nearby vegetation.",
    "hail": "Roof, window, siding, and vehicle damage caused by hailstorms.",
    "winter_weather": "Freeze, snow, ice, pipe damage, roof load, and power outage exposure.",
    "tornado": "Severe rotating wind risk affecting structure, roof, windows, and safe-room planning.",
    "urban_flooding": "Street, basement, yard, and stormwater flooding in developed areas.",
    "landslide": "Slope movement risk in hilly, mountainous, or saturated terrain.",
}

STATE_HAZARD_PROFILE = {
    "FL": {
        "hurricane_wind": 9, "storm_surge": 8, "flood": 8, "extreme_heat": 7,
        "tornado": 4, "wildfire": 3, "hail": 3, "winter_weather": 2,
        "urban_flooding": 4, "earthquake": 1,
    },
    "TX": {
        "hurricane_wind": 7, "flood": 8, "extreme_heat": 8, "hail": 6,
        "tornado": 6, "winter_weather": 3, "wildfire": 3, "urban_flooding": 4,
        "earthquake": 2,
    },
    "CA": {
        "earthquake": 9, "wildfire": 8, "extreme_heat": 6, "flood": 3,
        "landslide": 4, "hail": 2, "winter_weather": 2, "hurricane_wind": 1,
        "tornado": 1,
    },
    "CO": {
        "hail": 9, "wildfire": 6, "winter_weather": 7, "flood": 4,
        "extreme_heat": 4, "tornado": 3, "earthquake": 2, "hurricane_wind": 1,
    },
    "IL": {
        "winter_weather": 7, "urban_flooding": 6, "tornado": 6, "hail": 5,
        "extreme_heat": 4, "flood": 4, "hurricane_wind": 2, "earthquake": 2,
    },
    "DC": {
        "urban_flooding": 6, "flood": 5, "extreme_heat": 6, "winter_weather": 4,
        "hurricane_wind": 4, "tornado": 3, "hail": 3, "earthquake": 2,
    },
    "NC": {
        "hurricane_wind": 6, "flood": 6, "tornado": 5, "extreme_heat": 5,
        "winter_weather": 3, "hail": 3, "wildfire": 3, "earthquake": 2,
    },
    "ND": {
        "winter_weather": 9, "hail": 7, "tornado": 5, "flood": 4,
        "extreme_heat": 3, "wildfire": 3, "hurricane_wind": 1, "earthquake": 1,
    },
    "TN": {
        "tornado": 7, "flood": 6, "hurricane_wind": 3, "winter_weather": 4,
        "extreme_heat": 5, "hail": 5, "wildfire": 3, "earthquake": 2,
    },
    "WA": {
        "earthquake": 7, "flood": 6, "wildfire": 5, "winter_weather": 4,
        "landslide": 5, "extreme_heat": 3, "urban_flooding": 4,
        "hurricane_wind": 1, "hail": 2,
    },
}

CITY_ADJUSTMENTS = {
    "tampa": {"hurricane_wind": 1, "storm_surge": 1, "flood": 1, "extreme_heat": 1},
    "st. augustine": {"hurricane_wind": 1, "storm_surge": 1, "flood": 1},
    "saint augustine": {"hurricane_wind": 1, "storm_surge": 1, "flood": 1},
    "houston": {"flood": 2, "hurricane_wind": 1, "extreme_heat": 1},
    "los angeles": {"earthquake": 1, "wildfire": 1, "extreme_heat": 1},
    "denver": {"hail": 1, "winter_weather": 1, "wildfire": 1},
    "chicago": {"urban_flooding": 1, "winter_weather": 1},
    "washington": {"urban_flooding": 1, "extreme_heat": 1},
    "charlotte": {"flood": 1, "tornado": 1, "hurricane_wind": 1},
    "bismarck": {"winter_weather": 1, "hail": 1},
    "brentwood": {"tornado": 1, "flood": 1},
    "seattle": {"earthquake": 1, "flood": 1, "landslide": 1},
}

RETROFITS = {
    "Install flood sensors": {
        "base_points": 3, "hazards": ["flood", "storm_surge", "urban_flooding"],
        "cost_min": 50, "cost": "$50–$200", "priority": "High ROI",
    },
    "Improve drainage around the home": {
        "base_points": 7, "hazards": ["flood", "urban_flooding", "storm_surge"],
        "cost_min": 300, "cost": "$300–$3,000", "priority": "High ROI",
    },
    "Install hurricane shutters": {
        "base_points": 8, "hazards": ["hurricane_wind", "tornado"],
        "cost_min": 1500, "cost": "$1,500–$5,000", "priority": "High impact",
    },
    "Reinforce garage door": {
        "base_points": 6, "hazards": ["hurricane_wind", "tornado", "hail"],
        "cost_min": 500, "cost": "$500–$2,500", "priority": "High ROI",
    },
    "Add roof-to-wall connectors / roof straps": {
        "base_points": 7, "hazards": ["hurricane_wind", "tornado", "earthquake"],
        "cost_min": 1000, "cost": "$1,000–$3,500", "priority": "High impact",
    },
    "Install impact-rated windows": {
        "base_points": 10, "hazards": ["hurricane_wind", "tornado", "hail"],
        "cost_min": 15000, "cost": "$15,000–$40,000", "priority": "Major upgrade",
    },
    "Elevate HVAC/electrical systems": {
        "base_points": 6, "hazards": ["flood", "storm_surge", "urban_flooding"],
        "cost_min": 2000, "cost": "$2,000–$8,000", "priority": "Case-specific",
    },
    "Foundation bolting / seismic retrofit": {
        "base_points": 9, "hazards": ["earthquake"],
        "cost_min": 3000, "cost": "$3,000–$10,000+", "priority": "High impact",
    },
    "Brace water heater and secure heavy furniture": {
        "base_points": 4, "hazards": ["earthquake"],
        "cost_min": 50, "cost": "$50–$500", "priority": "High ROI",
    },
    "Create defensible space around property": {
        "base_points": 7, "hazards": ["wildfire"],
        "cost_min": 0, "cost": "$0–$2,500", "priority": "High ROI",
    },
    "Install ember-resistant vents": {
        "base_points": 6, "hazards": ["wildfire"],
        "cost_min": 300, "cost": "$300–$2,000", "priority": "High impact",
    },
    "Upgrade to impact-resistant roofing": {
        "base_points": 8, "hazards": ["hail", "hurricane_wind", "tornado"],
        "cost_min": 8000, "cost": "$8,000–$25,000+", "priority": "High impact",
    },
    "Insulate exposed pipes": {
        "base_points": 5, "hazards": ["winter_weather"],
        "cost_min": 50, "cost": "$50–$500", "priority": "High ROI",
    },
    "Add backup power / battery system": {
        "base_points": 5, "hazards": ["winter_weather", "hurricane_wind", "wildfire", "extreme_heat"],
        "cost_min": 500, "cost": "$500–$10,000+", "priority": "Broad benefit",
    },
    "Improve attic insulation and cooling efficiency": {
        "base_points": 5, "hazards": ["extreme_heat", "winter_weather"],
        "cost_min": 500, "cost": "$500–$4,000", "priority": "Broad benefit",
    },
}

BUDGETS = {
    "No budget selected": None,
    "Under $500": 500,
    "$2,000": 2000,
    "$5,000": 5000,
    "$10,000": 10000,
    "$25,000+": 25000,
}

FAMILY_ITEMS = {
    "Emergency kit prepared": 12,
    "Evacuation / shelter plan": 12,
    "Digital copies of important documents": 10,
    "Weather alerts enabled": 8,
    "Backup power or charging plan": 10,
    "3-day water and food supply": 12,
    "Insurance documents reviewed": 10,
    "Family communication plan": 8,
    "Medication / pet supplies plan": 8,
    "Basic first-aid supplies": 10,
}


def get_component(components, component_type, short=False):
    for component in components:
        if component_type in component.get("types", []):
            return component.get("short_name" if short else "long_name", "")
    return ""


@st.cache_data(show_spinner=False)
def geocode_address(address):
    if not GOOGLE_MAPS_API_KEY:
        return {"success": False, "error": "Missing GOOGLE_MAPS_API_KEY in .env file.", "candidates": []}

    if not address or not address.strip():
        return {"success": False, "error": "Empty address.", "candidates": []}

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
        return {"success": False, "error": str(e), "candidates": []}

    if data.get("status") != "OK":
        return {"success": False, "error": data.get("status", "Unknown error"), "candidates": []}

    candidates = []

    for result in data.get("results", []):
        components = result.get("address_components", [])
        location = result.get("geometry", {}).get("location", {})

        city = (
            get_component(components, "locality")
            or get_component(components, "sublocality")
            or get_component(components, "administrative_area_level_2")
        )

        state = get_component(components, "administrative_area_level_1", short=True)
        zip_code = get_component(components, "postal_code")

        candidates.append({
            "formatted_address": result.get("formatted_address", ""),
            "city": city,
            "state": state,
            "zip": zip_code,
            "lat": location.get("lat"),
            "lng": location.get("lng"),
        })

    return {"success": True, "candidates": candidates}


@st.cache_data(show_spinner=False)
def get_streetview_url(lat, lng):
    if not GOOGLE_MAPS_API_KEY or lat is None or lng is None:
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

    return (
        "https://maps.googleapis.com/maps/api/streetview"
        f"?size=800x500"
        f"&location={lat},{lng}"
        f"&fov=80"
        f"&pitch=0"
        f"&key={GOOGLE_MAPS_API_KEY}"
    )


def extract_state(address):
    if not address:
        return ""
    upper = address.upper()
    for state in STATE_NAMES:
        if re.search(rf"\b{state}\b", upper):
            return state
    return ""


def extract_city(address):
    if not address:
        return ""
    parts = [p.strip() for p in address.split(",")]
    if len(parts) >= 3:
        return parts[-3].lower()
    return ""


def get_hazard_profile(state, city):
    profile = {
        "flood": 4,
        "hurricane_wind": 2,
        "earthquake": 2,
        "wildfire": 3,
        "hail": 3,
        "winter_weather": 3,
        "extreme_heat": 4,
        "tornado": 3,
        "urban_flooding": 3,
    }

    if state in STATE_HAZARD_PROFILE:
        profile.update(STATE_HAZARD_PROFILE[state])

    city_lower = city.lower() if city else ""

    for city_key, adjustments in CITY_ADJUSTMENTS.items():
        if city_key in city_lower:
            for hazard, add in adjustments.items():
                profile[hazard] = min(10, profile.get(hazard, 0) + add)

    return profile


def top_hazards(profile, n=3):
    return sorted(profile.items(), key=lambda x: x[1], reverse=True)[:n]


def risk_level(value):
    if value >= 8:
        return "High"
    if value >= 6:
        return "Moderate-High"
    if value >= 4:
        return "Moderate"
    if value >= 2:
        return "Low-Moderate"
    return "Low"


def calculate_base_score(profile):
    top = top_hazards(profile, 5)
    weights = [2.4, 2.0, 1.5, 1.0, 0.7]
    penalty = sum(value * weights[i] for i, (_, value) in enumerate(top))
    score = 100 - penalty - 8 - 5
    return max(25, min(90, round(score)))


def score_label(score):
    if score < 45:
        return "High Risk"
    if score < 60:
        return "High Vulnerability"
    if score < 80:
        return "Moderate Resilience"
    return "Strong Resilience"


def retrofit_points(data, profile):
    max_risk = max([profile.get(h, 0) for h in data["hazards"]], default=0)

    if max_risk >= 8:
        multiplier = 1.0
    elif max_risk >= 6:
        multiplier = 0.8
    elif max_risk >= 4:
        multiplier = 0.55
    elif max_risk >= 2:
        multiplier = 0.3
    else:
        multiplier = 0.15

    return max(1, round(data["base_points"] * multiplier))


def create_gauge(score, title):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"suffix": "/100"},
        title={"text": title},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#2563eb"},
            "steps": [
                {"range": [0, 45], "color": "#fee2e2"},
                {"range": [45, 60], "color": "#ffedd5"},
                {"range": [60, 80], "color": "#fef3c7"},
                {"range": [80, 100], "color": "#dcfce7"},
            ],
        }
    ))
    fig.update_layout(height=260, margin=dict(l=20, r=20, t=50, b=10))
    return fig


def budget_plan(profile, budget):
    if budget is None:
        return [], 0, 0

    candidates = []

    for name, data in RETROFITS.items():
        pts = retrofit_points(data, profile)
        cost = max(1, data["cost_min"])
        roi = pts / cost

        if cost <= budget:
            candidates.append({
                "Upgrade": name,
                "Points": pts,
                "Minimum Cost": cost,
                "Cost Range": data["cost"],
                "Priority": data["priority"],
                "ROI": roi,
            })

    candidates = sorted(candidates, key=lambda x: (x["ROI"], x["Points"]), reverse=True)

    selected = []
    spent = 0
    gained = 0

    for item in candidates:
        if spent + item["Minimum Cost"] <= budget:
            selected.append(item)
            spent += item["Minimum Cost"]
            gained += item["Points"]

    return selected, spent, gained
def get_score_breakdown(profile):
    top = top_hazards(profile, 5)
    weights = [2.4, 2.0, 1.5, 1.0, 0.7]

    rows = []

    for i, (hazard, value) in enumerate(top):
        penalty = round(value * weights[i], 1)

        rows.append({
            "Score Factor": HAZARD_LABELS.get(hazard, hazard),
            "Hazard Intensity": f"{value}/10",
            "Score Impact": f"-{penalty}",
            "Reason": "Higher local hazard intensity reduces the current resilience score."
        })

    rows.append({
        "Score Factor": "Unknown building condition",
        "Hazard Intensity": "Unknown",
        "Score Impact": "-8",
        "Reason": "Roof age, roof shape, openings, drainage, and structural details are not verified yet."
    })

    rows.append({
        "Score Factor": "Data uncertainty",
        "Hazard Intensity": "Prototype",
        "Score Impact": "-5",
        "Reason": "This prototype does not yet include FEMA flood zones, county permits, elevation, or roof records."
    })

    return rows


def get_confidence_level(city, state, zip_code, lat, lng, streetview_available):
    score = 0
    reasons = []

    if city:
        score += 20
        reasons.append("City detected")
    if state:
        score += 20
        reasons.append("State detected")
    if zip_code:
        score += 15
        reasons.append("ZIP code detected")
    if lat is not None and lng is not None:
        score += 25
        reasons.append("Coordinates resolved")
    if streetview_available:
        score += 20
        reasons.append("Street View snapshot available")

    if score >= 80:
        level = "High-Medium"
    elif score >= 55:
        level = "Medium"
    elif score >= 30:
        level = "Low-Medium"
    else:
        level = "Low"

    explanation = ", ".join(reasons) if reasons else "Address details were not fully resolved."

    limitation = (
        "Property-level FEMA, flood-zone, elevation, permit, roof-age, and engineering inspection data "
        "are not connected yet."
    )

    return level, explanation, limitation


def get_roi_ranking(profile):
    rows = []

    for name, data in RETROFITS.items():
        points = retrofit_points(data, profile)
        min_cost = max(1, data["cost_min"])
        roi_score = round((points / min_cost) * 1000, 2)

        if roi_score >= 20:
            roi_label = "Very High ROI"
        elif roi_score >= 8:
            roi_label = "High ROI"
        elif roi_score >= 2:
            roi_label = "Moderate ROI"
        else:
            roi_label = "Lower ROI / Major Upgrade"

        rows.append({
            "Upgrade": name,
            "Score Gain": f"+{points}",
            "Estimated Cost": data["cost"],
            "Minimum Cost Used": f"${min_cost:,}",
            "ROI Category": roi_label,
            "Priority": data["priority"],
            "ROI Score": roi_score,
        })

    return sorted(rows, key=lambda x: x["ROI Score"], reverse=True)


def get_upgrade_roadmap(profile):
    hazards = [h for h, _ in top_hazards(profile, 3)]

    first_7_days = [
        "Save photos of the current property condition.",
        "Enable emergency and weather alerts.",
        "Review home insurance documents.",
    ]

    next_30_days = [
        "Schedule a basic home resilience walkthrough.",
        "Identify the highest-risk weak points around the home.",
        "Get at least one contractor estimate for the top recommended upgrade.",
    ]

    before_season = [
        "Complete the highest-ROI upgrades first.",
        "Update the family emergency plan.",
        "Re-check the resilience score after improvements."
    ]

    if "flood" in hazards or "storm_surge" in hazards or "urban_flooding" in hazards:
        first_7_days.append("Check gutters, downspouts, and visible drainage paths.")
        next_30_days.append("Install flood sensors in low or vulnerable areas.")
        before_season.append("Improve grading, drainage, or elevate vulnerable systems if needed.")

    if "hurricane_wind" in hazards or "tornado" in hazards:
        first_7_days.append("Check whether windows, doors, and garage door have visible protection.")
        next_30_days.append("Inspect garage door strength and roof connection vulnerabilities.")
        before_season.append("Consider shutters, garage reinforcement, roof straps, or impact-rated openings.")

    if "earthquake" in hazards:
        first_7_days.append("Locate gas, water, and electrical shutoff points.")
        next_30_days.append("Brace water heater and secure heavy furniture.")
        before_season.append("Evaluate foundation bolting or seismic retrofit options.")

    if "wildfire" in hazards:
        first_7_days.append("Remove dry leaves and flammable debris near the structure.")
        next_30_days.append("Trim vegetation and create defensible space.")
        before_season.append("Consider ember-resistant vents and fire-resistant exterior upgrades.")

    if "hail" in hazards:
        first_7_days.append("Check roof and gutters for visible damage.")
        next_30_days.append("Review roof age and condition.")
        before_season.append("Consider impact-resistant roofing when replacement is needed.")

    if "winter_weather" in hazards:
        first_7_days.append("Identify exposed pipes and freezing vulnerabilities.")
        next_30_days.append("Insulate exposed pipes and prepare backup heat or charging.")
        before_season.append("Prepare for freeze, snow, ice, and power outage exposure.")

    if "extreme_heat" in hazards:
        first_7_days.append("Check HVAC filters and cooling performance.")
        next_30_days.append("Improve shade, attic insulation, and cooling efficiency.")
        before_season.append("Prepare backup cooling or power options.")

    return {
        "First 7 Days": first_7_days[:5],
        "Next 30 Days": next_30_days[:5],
        "Before Next Hazard Season": before_season[:5],
    }


def get_professional_questions(profile):
    hazards = [h for h, _ in top_hazards(profile, 3)]

    contractor = [
        "Which upgrade would reduce the most risk for the lowest cost?",
        "Are there visible roof, drainage, window, door, or garage vulnerabilities?",
    ]

    insurance = [
        "Are there mitigation discounts for completed resilience upgrades?",
        "Are there hazard-specific coverage gaps for this property?",
    ]

    inspector = [
        "What are the weakest points of this home during the top local hazard event?",
        "Are there signs of drainage, roof, foundation, or opening-protection issues?",
    ]

    if "flood" in hazards or "storm_surge" in hazards or "urban_flooding" in hazards:
        contractor.append("Where does water flow during heavy rain, and how can drainage be improved?")
        insurance.append("Should this property carry separate flood insurance even if it is not required?")
        inspector.append("Is the HVAC, electrical equipment, or entry level vulnerable to floodwater?")

    if "hurricane_wind" in hazards or "tornado" in hazards:
        contractor.append("Is the garage door wind-rated or should it be reinforced?")
        contractor.append("Can roof-to-wall connectors or roof straps be inspected or upgraded?")
        insurance.append("Do shutters, impact windows, roof straps, or garage reinforcement qualify for discounts?")
        inspector.append("Are openings protected against windborne debris?")

    if "earthquake" in hazards:
        contractor.append("Is foundation bolting recommended for this structure?")
        insurance.append("Is earthquake coverage separate from standard homeowners insurance?")
        inspector.append("Is the water heater braced and are heavy interior items secured?")

    if "wildfire" in hazards:
        contractor.append("Can defensible space or ember-resistant vents be added?")
        insurance.append("Are wildfire mitigation upgrades recognized by the insurer?")
        inspector.append("Are gutters, vents, vegetation, or exterior materials vulnerable to embers?")

    return {
        "Contractor Questions": contractor[:5],
        "Insurance Questions": insurance[:5],
        "Home Inspector Questions": inspector[:5],
    }
def safe_text(value):
    if value is None:
        return ""
    return str(value).replace("–", "-").replace("—", "-").replace("’", "'").replace("“", '"').replace("”", '"')


def generate_pdf_report(
    address,
    city,
    state,
    zip_code,
    streetview_url,
    top_three,
    profile,
    base_score,
    after_score,
    family_score,
    score_rows,
    confidence_level,
    confidence_reason,
    confidence_limitation,
    roi_rows,
    roadmap,
    questions,
    selected_budget_label,
    plan,
    spent,
    gained,
):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    left = 12
    width = 180

    def clean(value):
        if value is None:
            return ""
        text = str(value)
        text = text.replace("–", "-").replace("—", "-")
        text = text.replace("’", "'").replace("“", '"').replace("”", '"')
        text = text.replace("•", "-")
        text = text.encode("latin-1", "replace").decode("latin-1")
        return text

    def write_line(text="", size=10, bold=False, height=6):
        pdf.set_x(left)
        pdf.set_font("Helvetica", "B" if bold else "", size)
        pdf.multi_cell(width, height, clean(text))

    def section_title(title):
        pdf.ln(3)
        write_line(title, size=14, bold=True, height=8)

    def bullet(text):
        write_line(f"- {text}", size=10, bold=False, height=6)

    # Header
    write_line("HazardShield AI", size=20, bold=True, height=10)
    write_line("Property Resilience Report | Educational Prototype", size=11, height=7)
    pdf.ln(3)

    # Property Overview
    section_title("Property Overview")
    write_line(f"Address: {address}", size=11)
    write_line(f"City: {city if city else 'Unknown'}", size=11)
    write_line(f"State: {state if state else 'Unknown'}", size=11)
    write_line(f"ZIP: {zip_code if zip_code else 'Unknown'}", size=11)

    # Top Hazards
    section_title("Top Natural Hazards")
    for idx, hazard_item in enumerate(top_three, start=1):
        hazard, value = hazard_item
        hazard_name = HAZARD_LABELS.get(hazard, hazard)
        level = risk_level(value)
        write_line(f"{idx}. {hazard_name} - {value}/10 - {level}", size=10)

    # Scores
    section_title("Resilience Scores")
    write_line(f"Current Score: {base_score}/100 - {score_label(base_score)}", size=11)
    write_line(f"After Manual Upgrades: {after_score}/100", size=11)
    write_line(f"Manual Improvement: +{after_score - base_score} points", size=11)
    write_line(f"Family Readiness Score: {family_score}/100", size=11)

    # Why This Score
    section_title("Why This Score?")
    for row in score_rows:
        factor = row.get("Score Factor", "")
        impact = row.get("Score Impact", "")
        reason = row.get("Reason", "")
        bullet(f"{factor}: {impact} points. {reason}")

    # Confidence
    section_title("Model Confidence")
    write_line(f"Confidence Level: {confidence_level}", size=11)
    write_line(f"Reason: {confidence_reason}", size=10)
    write_line(f"Limitation: {confidence_limitation}", size=10)

    # ROI
    section_title("Best Upgrades by Resilience ROI")
    for row in roi_rows[:7]:
        upgrade = row.get("Upgrade", "")
        gain = row.get("Score Gain", "")
        cost = row.get("Estimated Cost", "")
        roi = row.get("ROI Category", "")
        bullet(f"{upgrade}: {gain}, {cost}, {roi}")

    # Budget Plan
    section_title("Budget-Based Upgrade Plan")

    safe_spent = spent if spent is not None else 0
    safe_gained = gained if gained is not None else 0

    write_line(
        f"Selected Budget: {selected_budget_label} | Minimum Spend: ${safe_spent:,} | Estimated Gain: +{safe_gained} points",
        size=10
    )

    if plan:
        for item in plan:
            upgrade = item.get("Upgrade", "")
            points = item.get("Points", "")
            cost_range = item.get("Cost Range", "")
            bullet(f"{upgrade}: +{points} points, {cost_range}")
    else:
        write_line("No budget-based upgrade plan selected.", size=10)

    # Roadmap
    section_title("Upgrade Roadmap")
    for phase, items in roadmap.items():
        write_line(phase, size=11, bold=True)
        for item in items:
            bullet(item)

    # Questions
    section_title("Questions to Ask Professionals")
    for section, items in questions.items():
        write_line(section, size=11, bold=True)
        for item in items:
            bullet(item)

    # Data Sources
    section_title("Data Sources and Limitations")
    write_line(
        "Current sources: Google Geocoding API, Google Street View Static API, built-in regional hazard scoring model, user-selected retrofit simulator, and family readiness checklist.",
        size=10
    )
    write_line(
        "Not connected yet: FEMA National Risk Index, FEMA flood zones, NOAA storm history, USGS elevation data, county property records, roof age, permit history, and computer vision from property imagery.",
        size=10
    )

    # Disclaimer
    section_title("Disclaimer")
    write_line(
        "HazardShield AI is an educational prototype. It is not a formal engineering inspection, official hazard certification, insurance determination, or safety guarantee.",
        size=9
    )

    pdf_bytes = pdf.output(dest="S")

    if isinstance(pdf_bytes, str):
        pdf_bytes = pdf_bytes.encode("latin-1")

    if isinstance(pdf_bytes, bytearray):
        pdf_bytes = bytes(pdf_bytes)

    return pdf_bytes
# ============================================================
# Sidebar
# ============================================================

with st.sidebar:
    st.title("🛡️ HazardShield AI")
    st.caption("Natural hazard resilience optimizer")

    manual_address = st.text_input(
        "Enter property address",
        placeholder="Enter a U.S. property address"
    )

    raw_address = manual_address.strip()

    selected_budget_label = st.selectbox("Budget Mode", list(BUDGETS.keys()))
    selected_budget = BUDGETS[selected_budget_label]


# ============================================================
# Address resolving
# ============================================================

st.title("🛡️ HazardShield AI")
st.write("Address-based natural hazard resilience optimizer.")

if not raw_address:
    st.info("Enter a U.S. address in the sidebar or select a test address.")
    st.stop()

geocoded = geocode_address(raw_address)

if geocoded.get("success") and geocoded.get("candidates"):
    candidates = geocoded["candidates"][:5]

    if len(candidates) > 1:
        options = [c["formatted_address"] for c in candidates]
        chosen_address = st.selectbox("Which address did you mean?", options)
        selected_candidate = candidates[options.index(chosen_address)]
    else:
        selected_candidate = candidates[0]

    address = selected_candidate["formatted_address"]
    city = selected_candidate["city"]
    state = selected_candidate["state"]
    zip_code = selected_candidate["zip"]
    lat = selected_candidate["lat"]
    lng = selected_candidate["lng"]

else:
    st.warning(f"Google could not resolve this address: {geocoded.get('error', 'Unknown error')}")
    address = raw_address
    city = extract_city(address)
    state = extract_state(address)
    zip_code = ""
    lat = None
    lng = None


profile = get_hazard_profile(state, city)
base_score = calculate_base_score(profile)
top_three = top_hazards(profile, 3)
top_driver = top_three[0][0]

# ============================================================
# Main layout
# ============================================================

left, right = st.columns([1.3, 1])

with left:
    st.subheader("Property Overview")
    st.write(f"**Address:** {address}")
    st.write(f"**City:** {city if city else 'Unknown'}")
    st.write(f"**State:** {STATE_NAMES.get(state, 'Unknown')}")
    st.write(f"**ZIP:** {zip_code if zip_code else 'Unknown'}")
    st.info(f"Top Risk Driver: **{HAZARD_LABELS.get(top_driver, top_driver)}**")

with right:
    st.subheader("Property Snapshot")
    streetview = get_streetview_url(lat, lng)

    if streetview:
        st.image(streetview, caption=address, use_container_width=True)
    else:
        st.info("Street View image unavailable for this address.")

st.divider()

# ============================================================
# Sidebar dependent widgets
# ============================================================

with st.sidebar:
    st.markdown("---")
    st.subheader("Family Readiness Checklist")

    family_score = 0
    for item, points in FAMILY_ITEMS.items():
        if st.checkbox(item, key=f"family_{item}"):
            family_score += points

    family_score = min(100, family_score)

    st.markdown("---")
    st.subheader("Manual Retrofit Simulator")

    selected_retrofits = []
    after_score = base_score

    for name, data in RETROFITS.items():
        pts = retrofit_points(data, profile)
        if st.checkbox(f"{name} (+{pts})", key=f"retrofit_{name}"):
            selected_retrofits.append(name)
            after_score += pts

    after_score = min(100, after_score)

# ============================================================
# Hazards
# ============================================================

st.subheader("Top Natural Hazards")

cols = st.columns(3)

for idx, (hazard, value) in enumerate(top_three):
    with cols[idx]:
        st.metric(
            label=f"#{idx + 1} {HAZARD_LABELS.get(hazard, hazard)}",
            value=f"{value}/10",
            delta=risk_level(value)
        )
        st.caption(HAZARD_DESCRIPTIONS.get(hazard, ""))

st.divider()

# ============================================================
# Scores
# ============================================================

st.subheader("Resilience Scores")

score_col1, score_col2, score_col3 = st.columns(3)

with score_col1:
    st.plotly_chart(create_gauge(base_score, "Current Score"), use_container_width=True)
    st.write(f"**{score_label(base_score)}**")

with score_col2:
    st.plotly_chart(create_gauge(after_score, "After Manual Upgrades"), use_container_width=True)
    st.write(f"**Improvement:** +{after_score - base_score} points")

with score_col3:
    st.plotly_chart(create_gauge(family_score, "Family Readiness"), use_container_width=True)
    st.write("Based on the checklist in the sidebar.")

st.divider()

# ============================================================
# Budget optimizer
# ============================================================

st.subheader("Budget-Based Upgrade Optimizer")

plan, spent, gained = budget_plan(profile, selected_budget)

if selected_budget is None:
    st.info("Select a budget in the sidebar to generate an optimized upgrade plan.")
else:
    st.success(
        f"Budget: {selected_budget_label} | Minimum spend: ${spent:,} | "
        f"Estimated score gain: +{gained} points | "
        f"Score: {base_score}/100 → {min(100, base_score + gained)}/100"
    )

    if plan:
        st.dataframe(pd.DataFrame(plan).drop(columns=["ROI"]), use_container_width=True, hide_index=True)
    else:
        st.warning("No upgrades fit inside this budget.")

st.divider()

# ============================================================
# Hazard breakdown
# ============================================================
# ============================================================
# Professional analysis blocks
# ============================================================

st.subheader("Why This Score?")

score_rows = get_score_breakdown(profile)

st.write(
    "This section explains how the current resilience score is reduced by the strongest local hazards "
    "and by missing property-level information."
)

st.dataframe(
    pd.DataFrame(score_rows),
    use_container_width=True,
    hide_index=True
)

st.divider()

st.subheader("Model Confidence")

confidence_level, confidence_reason, confidence_limitation = get_confidence_level(
    city=city,
    state=state,
    zip_code=zip_code,
    lat=lat,
    lng=lng,
    streetview_available=streetview is not None
)

conf_col1, conf_col2 = st.columns(2)

with conf_col1:
    st.metric("Confidence Level", confidence_level)
    st.write(confidence_reason)

with conf_col2:
    st.warning(confidence_limitation)

st.divider()

st.subheader("Best Upgrades by Resilience ROI")

roi_rows = get_roi_ranking(profile)

st.write(
    "This ranks upgrades by estimated score gain compared with minimum estimated cost. "
    "Low-cost upgrades with meaningful score improvement appear first."
)

roi_display = pd.DataFrame(roi_rows).drop(columns=["ROI Score"])
st.dataframe(roi_display, use_container_width=True, hide_index=True)

st.divider()

st.subheader("Upgrade Roadmap")

roadmap = get_upgrade_roadmap(profile)

roadmap_cols = st.columns(3)

for index, (phase, items) in enumerate(roadmap.items()):
    with roadmap_cols[index]:
        st.markdown(f"### {phase}")
        for item in items:
            st.write(f"• {item}")

st.divider()

st.subheader("Questions to Ask Professionals")

questions = get_professional_questions(profile)

q_cols = st.columns(3)

for index, (section, items) in enumerate(questions.items()):
    with q_cols[index]:
        st.markdown(f"### {section}")
        for item in items:
            st.write(f"• {item}")

st.divider()


# ============================================================
# PDF Report
# ============================================================

st.subheader("Download Property Resilience Report")

pdf_bytes = generate_pdf_report(
    address=address,
    city=city,
    state=state,
    zip_code=zip_code,
    streetview_url=streetview,
    top_three=top_three,
    profile=profile,
    base_score=base_score,
    after_score=after_score,
    family_score=family_score,
    score_rows=score_rows,
    confidence_level=confidence_level,
    confidence_reason=confidence_reason,
    confidence_limitation=confidence_limitation,
    roi_rows=roi_rows,
    roadmap=roadmap,
    questions=questions,
    selected_budget_label=selected_budget_label,
    plan=plan,
    spent=spent,
    gained=gained,
)

st.download_button(
    label="Download PDF Report",
    data=pdf_bytes,
    file_name="hazardshield_property_resilience_report.pdf",
    mime="application/pdf"
)

st.divider()
st.subheader("Hazard Intensity Breakdown")

for hazard, value in sorted(profile.items(), key=lambda x: x[1], reverse=True):
    st.write(f"**{HAZARD_LABELS.get(hazard, hazard)}** — {value}/10 — {risk_level(value)}")
    st.progress(value / 10)
    st.caption(HAZARD_DESCRIPTIONS.get(hazard, ""))

st.divider()

# ============================================================
# Manual upgrades
# ============================================================

st.subheader("Manual Selected Upgrades")

if selected_retrofits:
    rows = []
    for name in selected_retrofits:
        data = RETROFITS[name]
        rows.append({
            "Upgrade": name,
            "Score Impact": f"+{retrofit_points(data, profile)}",
            "Estimated Cost": data["cost"],
            "Priority": data["priority"],
        })

    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
else:
    st.info("No manual upgrades selected yet.")

st.divider()

# ============================================================
# Action plan
# ============================================================

st.subheader("Personalized Action Plan")

hazards = [h for h, _ in top_three]

if "hurricane_wind" in hazards or "tornado" in hazards:
    st.write("✅ Prioritize wind protection: garage door reinforcement, shutters, impact windows, and roof connections.")

if "flood" in hazards or "storm_surge" in hazards or "urban_flooding" in hazards:
    st.write("✅ Prioritize water management: drainage improvements, flood sensors, and elevation of vulnerable systems.")

if "earthquake" in hazards:
    st.write("✅ Prioritize seismic safety: foundation bolting, water heater straps, and securing heavy furniture.")

if "wildfire" in hazards:
    st.write("✅ Prioritize wildfire mitigation: defensible space, ember-resistant vents, and vegetation management.")

if "hail" in hazards:
    st.write("✅ Prioritize roof resilience: inspect the roof and consider impact-resistant materials.")

if "winter_weather" in hazards:
    st.write("✅ Prioritize freeze protection: pipe insulation, backup heat/power, and winter readiness.")

if "extreme_heat" in hazards:
    st.write("✅ Prioritize heat resilience: HVAC maintenance, attic insulation, shade, and backup cooling/power.")

st.divider()

# ============================================================
# Location comparison
# ============================================================

st.subheader("Location Comparison")

compare_enabled = st.checkbox("Do you want to compare another address?")

if compare_enabled:
    compare_address_raw = st.text_input("Enter comparison address")

    if compare_address_raw:
        compare_geo = geocode_address(compare_address_raw)

        if compare_geo.get("success") and compare_geo.get("candidates"):
            c = compare_geo["candidates"][0]
            compare_profile = get_hazard_profile(c["state"], c["city"])
            compare_score = calculate_base_score(compare_profile)
            compare_top = top_hazards(compare_profile, 3)

            comparison_rows = [
                {
                    "Location": "Primary",
                    "Address": address,
                    "City": city,
                    "State": state,
                    "Top 3 Hazards": ", ".join([HAZARD_LABELS.get(h, h) for h, _ in top_three]),
                    "Score": base_score,
                },
                {
                    "Location": "Comparison",
                    "Address": c["formatted_address"],
                    "City": c["city"],
                    "State": c["state"],
                    "Top 3 Hazards": ", ".join([HAZARD_LABELS.get(h, h) for h, _ in compare_top]),
                    "Score": compare_score,
                },
            ]

            st.dataframe(pd.DataFrame(comparison_rows), use_container_width=True, hide_index=True)
        else:
            st.warning("Could not resolve the comparison address.")

st.divider()

st.caption(
    "HazardShield AI • Yegor Kanalin • Educational prototype. "
    "This tool is not a formal engineering inspection, official hazard certification, insurance determination, or safety guarantee."
)