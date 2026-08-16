# HazardShield AI

## Most homes are not disaster-ready. HazardShield AI shows exactly why — and what to fix first.

**HazardShield AI** is an address-based property resilience platform that analyzes natural hazard exposure, explains risk scores, ranks upgrade recommendations by ROI, and generates a personalized PDF resilience report.

Enter any U.S. address and get a disaster risk score, hazard breakdown, upgrade plan, family readiness checklist, confidence level, and downloadable resilience report in seconds.

---

## Why I Built This

Natural disasters are becoming more expensive, more frequent, and more personal. Most homeowners, renters, and buyers do not have an easy way to understand the risks around a property before they make important decisions.

HazardShield AI was built to make property risk easier to understand.

The goal is simple:

> Turn a normal home address into a clear, useful, and actionable resilience report.

---

## What HazardShield AI Does

HazardShield AI helps users answer questions like:

* What natural hazards are most relevant to this property?
* How resilient is this home right now?
* Why did the property receive this score?
* Which upgrades should be prioritized first?
* Which upgrades give the best resilience return on investment?
* How prepared is the family for an emergency?
* What should I ask a contractor, inspector, or insurance professional?
* Can I download a professional-looking PDF report?

---

## Key Features

### Address-Based Risk Analysis

Users enter a property address, and the app uses Google Maps APIs to identify the location and evaluate regional hazard exposure.

### Google Street View Snapshot

When available, the app displays a Street View image of the property area to make the report more visual and property-specific.

### Natural Hazard Scoring

The app estimates exposure to hazards such as:

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

### Resilience Score

HazardShield AI generates a property resilience score from 0 to 100 based on local hazard intensity and prototype-level property assumptions.

### Why This Score?

The app explains what reduced the score, including top local hazards, missing property details, and data uncertainty.

### Model Confidence

The app shows how confident the model is based on detected address details, coordinates, ZIP code, and Street View availability.

### Upgrade ROI Ranking

Recommended upgrades are ranked by estimated score improvement compared with estimated minimum cost.

### Budget-Based Upgrade Plan

Users can choose a budget mode, and the app recommends the best combination of upgrades within that budget.

### Family Readiness Checklist

Users can check emergency preparedness items and receive a family readiness score.

### Upgrade Roadmap

The app creates a step-by-step action plan:

* First 7 days
* Next 30 days
* Before next hazard season

### Professional Questions

HazardShield AI generates questions to ask:

* Contractors
* Insurance professionals
* Home inspectors

### PDF Resilience Report

Users can download a personalized PDF report containing the property overview, hazard breakdown, scores, recommendations, confidence level, roadmap, and limitations.

---

## Tech Stack

* Python
* Streamlit
* Pandas
* Plotly
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
4. The app estimates natural hazard exposure based on state and city-level hazard profiles.
5. HazardShield AI calculates a resilience score.
6. The app explains why the score was assigned.
7. Recommended upgrades are ranked by score impact and estimated ROI.
8. The user can select a budget and generate an upgrade plan.
9. The app creates a personalized PDF resilience report.

---

## Example Use Cases

HazardShield AI could help:

* Homebuyers compare properties before making a decision
* Homeowners understand what upgrades to prioritize
* Renters evaluate disaster exposure before signing a lease
* Families improve emergency preparedness
* Insurance or inspection professionals explain risk more clearly
* Students and researchers explore property resilience modeling

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
* Online deployment
* More advanced scoring model
* Improved UI and report design

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

## Important Security Note

The Google Maps API key is stored locally in a `.env` file.

The `.env` file is intentionally excluded from GitHub using `.gitignore`.

Never upload API keys, secrets, or private credentials to a public repository.

---

## Project Status

Current version:

* Working Streamlit app
* Address input
* Google Maps geocoding
* Street View snapshot
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
* PDF report download

---

## Disclaimer

HazardShield AI is an educational prototype. It is not a formal engineering inspection, official hazard certification, insurance determination, or safety guarantee.
