# HazardShield AI

## Most homes are not disaster-ready. HazardShield AI shows exactly why — and what to fix first.

**HazardShield AI** is an address-based property resilience platform that turns any U.S. property address into a natural hazard risk score, hazard breakdown, upgrade plan, ROI ranking, and personalized PDF resilience report.

Enter an address. Get a clear disaster-risk profile in seconds.

---

## Live Demo

Try HazardShield AI here:

**https://hazardshield-ai.streamlit.app**

---

## What This Project Does

HazardShield AI helps users understand how exposed a property may be to natural hazards and what upgrades could improve its resilience.

The app analyzes a property address and generates:

* Natural hazard exposure profile
* Property resilience score
* Explanation of why the score was assigned
* Model confidence level
* Recommended upgrades
* Upgrade ROI ranking
* Budget-based improvement plan
* Family readiness checklist
* Professional questions for contractors, inspectors, and insurance providers
* Downloadable PDF resilience report

---

## Why I Built This

Natural disasters are becoming more expensive, more frequent, and more personal. Yet most homeowners, renters, and homebuyers do not have a simple way to understand property-level disaster risk before making important decisions.

A home may look safe from the outside, but still carry hidden exposure to flooding, hurricane wind, wildfire, storm surge, hail, extreme heat, or other hazards.

HazardShield AI was built to make this information easier to understand.

The goal is simple:

> Turn a normal home address into a clear, useful, and actionable resilience report.

---

## Key Features

### Address-Based Property Analysis

Users enter a U.S. property address, and the app uses Google Maps APIs to identify the location, city, state, ZIP code, latitude, and longitude.

### Google Street View Snapshot

When available, the app displays a Google Street View image of the property area to make the analysis more visual and location-specific.

### Natural Hazard Scoring

HazardShield AI estimates exposure to hazards such as:

* Hurricane wind
* Flooding
* Storm surge
* Wildfire
* Earthquake
* Tornado
* Hail
* Extreme heat
* Winter weather
* Urban flooding

### Property Resilience Score

The app calculates a resilience score from 0 to 100 based on regional hazard intensity and prototype-level property assumptions.

### Why This Score?

Instead of showing only a number, HazardShield AI explains the score by breaking down the factors that reduce resilience, including:

* Strongest local hazards
* Unknown building condition
* Data uncertainty
* Missing property-level details

### Model Confidence

The app shows how confident the model is based on detected address data, ZIP code, coordinates, and Street View availability.

### Upgrade ROI Ranking

Recommended improvements are ranked by estimated score gain compared with estimated minimum cost.

This helps answer:

> Which upgrade gives the most resilience improvement for the lowest cost?

### Budget-Based Upgrade Optimizer

Users can select a budget mode, and the app recommends the best upgrade combination within that budget.

### Family Readiness Checklist

The app includes a preparedness checklist and calculates a family readiness score based on emergency planning items.

### Upgrade Roadmap

HazardShield AI creates a phased action plan:

* First 7 days
* Next 30 days
* Before next hazard season

### Professional Questions

The app generates practical questions to ask:

* Contractors
* Insurance professionals
* Home inspectors

### PDF Resilience Report

Users can download a personalized PDF report that includes the property overview, hazard breakdown, resilience scores, upgrade plan, model confidence, professional questions, and limitations.

---

## Example Use Cases

HazardShield AI could help:

* Homebuyers compare properties before purchasing
* Homeowners decide which upgrades to prioritize
* Renters understand disaster exposure before signing a lease
* Families improve emergency preparedness
* Insurance professionals explain risk more clearly
* Home inspectors communicate resilience concerns
* Students explore property risk modeling and climate resilience

---

## Tech Stack

* Python
* Streamlit
* Pandas
* Plotly
* Requests
* Google Geocoding API
* Google Street View Static API
* fpdf2
* python-dotenv

---

## Project Structure

```text
hazardshield-ai/
│
├── app/
│   ├── streamlit_app.py
│   ├── geocoding.py
│   ├── streetview.py
│   ├── scoring_model.py
│   ├── recommendations.py
│   └── retrofit_simulator.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## How It Works

1. The user enters a U.S. property address.
2. Google Geocoding API resolves the address, city, state, ZIP code, latitude, and longitude.
3. Google Street View Static API attempts to display a property snapshot.
4. The app estimates natural hazard exposure using regional hazard profiles.
5. HazardShield AI calculates a resilience score.
6. The app explains why the score was assigned.
7. Recommended upgrades are ranked by estimated impact and ROI.
8. The user can select a budget and generate an upgrade plan.
9. The app creates a downloadable PDF resilience report.

---

## Current Limitations

HazardShield AI is currently an educational prototype.

It does not yet include:

* FEMA flood zones
* FEMA National Risk Index
* NOAA storm event history
* USGS elevation data
* County property records
* Roof age and permit history
* Real engineering inspection data
* Computer vision from property images

The app is designed to support resilience planning, not replace a licensed engineer, home inspector, insurance professional, or official hazard determination.

---

## Future Improvements

Planned improvements include:

* FEMA National Risk Index integration
* FEMA flood zone lookup
* NOAA storm history integration
* USGS elevation data
* Address-to-address comparison
* Computer vision property inspection prototype
* More detailed upgrade cost calculator
* Improved UI and report design
* More advanced scoring model
* Saved report history
* Expanded property-specific data sources

---

## Running the App Locally

Clone the repository:

```bash
git clone https://github.com/YegorKanalin/hazardshield-ai.git
cd hazardshield-ai
```

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Create a `.env` file in the project root:

```text
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
```

Run the app:

```bash
python3 -m streamlit run app/streamlit_app.py
```

---

## Security Note

The Google Maps API key is stored locally in a `.env` file and in Streamlit Cloud Secrets for deployment.

The `.env` file is excluded from GitHub using `.gitignore`.

Never upload API keys, secrets, or private credentials to a public repository.

---

## Project Status

Current version includes:

* Working online Streamlit deployment
* Address input
* Google Maps geocoding
* Google Street View snapshot
* Hazard scoring
* Resilience score
* Upgrade recommendations
* Budget optimizer
* Family readiness checklist
* Score explanation
* Model confidence
* ROI ranking
* Upgrade roadmap
* Professional questions
* Downloadable PDF report

---

## Disclaimer

HazardShield AI is an educational prototype. It is not a formal engineering inspection, official hazard certification, insurance determination, or safety guarantee.
