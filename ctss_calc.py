# CTSS Calculator – single‑file Streamlit app (required selections for Capability, Opportunity, Intent)
# -------------------------------------------------
# Run locally:
#   1) pip install streamlit
#   2) streamlit run ctss_app.py

import streamlit as st

st.set_page_config(page_title="CTSS Calculator", layout="wide")
st.title("CTSS Calculator (CTSSBase & CTSSEffort)")
st.caption("Single‑file prototype. Required selections for Capability, Opportunity, Intent. Effort may stay Unknown.")

# -----------------------------
# Score helpers
# -----------------------------

def ctss_calc(C: float, O: float, I: float, E: float, wI: float, wO: float) -> float:
    return (wI*I + wO*O) * (C / (C+E))

# -----------------------------
# Mappings from questionnaire options to numeric scores
# -----------------------------
# Capability
SKILLS = {
    "Narrow (≤10 ATT&CK sub‑techniques)": 0.30,
    "Moderate (11–24)": 0.60,
    "Broad (≥25)": 1.00,
    "Unknown": 0.50,
}
RES_C2 = {
    "< 1,000 IPs": 0.30,
    "1,000–10,000 IPs": 0.60,
    "> 10,000 IPs": 1.00,
    "Unknown": 0.50,
}
RES_0DAY = {
    "None": 0.30,
    "Occasional": 0.60,
    "Frequent": 1.00,
    "Unknown": 0.50,
}
TOOLING = {
    "Low: off‑the‑shelf only": 0.30,
    "Medium: commodity + custom scripts": 0.60,
    "High: bespoke frameworks / automation": 1.00,
    "Unknown": 0.50,
}
TRADECRAFT = {
    "Low: breakout >24h or dwell <7d": 0.30,
    "Medium: breakout 1m–24h or dwell 7–30d": 0.60,
    "High: breakout ≤60s or dwell >30d": 1.00,
    "Unknown": 0.50,
}

ACTOR_PRESETS = {
    "NationState": {
        "SKILLS": "Broad (≥25)",
        "RES_C2": "> 10,000 IPs",
        "RES_0DAY": "Frequent",
        "TOOLING": "High: bespoke frameworks / automation",
        "TRADECRAFT": "High: breakout ≤60s or dwell >30d",
    },
    "Cybercriminal": {
        "SKILLS": "Moderate (11–24)",
        "RES_C2": "1,000–10,000 IPs",
        "RES_0DAY": "Occasional",
        "TOOLING": "Medium: commodity + custom scripts",
        "TRADECRAFT": "Medium: breakout 1m–24h or dwell 7–30d",
    },
    "IdeologyDriven": {
        "SKILLS": "Moderate (11–24)",
        "RES_C2": "< 1,000 IPs",
        "RES_0DAY": "None",
        "TOOLING": "Low: off‑the‑shelf only",
        "TRADECRAFT": "Medium: breakout 1m–24h or dwell 7–30d",
    },
    "MaliciousInsider": {
        "SKILLS": "Moderate (11–24)",
        "RES_C2": "< 1,000 IPs",
        "RES_0DAY": "None",
        "TOOLING": "Medium: commodity + custom scripts",
        "TRADECRAFT": "High: breakout ≤60s or dwell >30d",
    },
}

# Opportunity
SURFACE_APPS = {
    "0–5": 0.10,
    "6–25": 0.25,
    "26–100": 0.50,
    "101–500": 0.75,
    "> 500": 1.00,
}
SURFACE_ENDPOINTS = {
    "0–5": 0.10,
    "6–25": 0.25,
    "26–100": 0.50,
    "101–500": 0.75,
    "> 500": 1.00,
}
SOCIAL_SIZE = {
    "1–249": 0.60,
    "250–1000": 0.80,
    "> 1000": 1.00,
}

# Intent
SECTOR = {
    "Finance": 1.00,
    "Technology/IT": 1.00,
    "Manufacturing": 1.00,
    "Government/public administration": 1.00,
    "Healthcare": 0.60,
    "Education": 0.60,
    "Energy": 0.60,
    "Transportation": 0.60,
    "Other": 0.30,
}
ASSET_VALUE = {
    "< $100k": 0.10,
    "$100k – $1M": 0.30,
    "$1M – $10M": 0.50,
    "$10M – $100M": 0.75,
    "> $100M": 1.00,
    "Cannot estimate": 0.50,
}
CRITICALITY = {
    "Minimal (< 99.00% uptime; > 24 h downtime / year)": 0.10,
    "Low (99.00% – 99.90% uptime; 9 – 24 h downtime / year)": 0.25,
    "Moderate (99.90% – 99.99% uptime; 1 – 9 h downtime / year)": 0.50,
    "High-availability (99.988% – 99.998% uptime; 10 – 60 min downtime / year)": 0.75,
    "Mission-critical (≥ 99.998% uptime; ≤ 10 min downtime / year)": 1.00,
}
GEO_RISK = {
    "Afghanistan": 0.56,
    "Albania": 0.35,
    "Algeria": 0.34,
    "Andorra": 0.21,
    "Angola": 0.45,
    "Antigua and Barbuda": 0.63,
    "Argentina": 0.37,
    "Armenia": 0.51,
    "Australia": 0.06,
    "Austria": 0.14,
    "Azerbaijan": 0.26,
    "Bahamas, The": 0.51,
    "Bahrain": 0.23,
    "Bangladesh": 0.37,
    "Barbados": 0.47,
    "Belarus": 0.40,
    "Belgium": 0.08,
    "Belize": 0.44,
    "Benin": 0.22,
    "Bhutan": 0.32,
    "Bolivia": 0.67,
    "Bosnia and Herzegovina": 0.43,
    "Botswana": 0.20,
    "Brazil": 0.26,
    "Brunei": 0.28,
    "Bulgaria": 0.27,
    "Burkina Faso": 0.46,
    "Burundi": 0.85,
    "Cabo Verde": 0.28,
    "Cambodia": 0.47,
    "Cameroon": 0.38,
    "Canada": 0.08,
    "Central African Republic": 0.62,
    "Chad": 0.69,
    "Chile": 0.21,
    "China": 0.36,
    "Colombia": 0.32,
    "Comoros": 0.47,
    "Congo, Dem. Rep.": 0.66,
    "Congo, Rep.": 0.77,
    "Costa Rica": 0.32,
    "Cote d'Ivoire": 0.27,
    "Croatia": 0.28,
    "Cuba": 0.28,
    "Cyprus": 0.14,
    "Czechia": 0.14,
    "Denmark": 0.00,
    "Djibouti": 0.72,
    "Dominica": 0.58,
    "Dominican Republic": 0.28,
    "Ecuador": 0.28,
    "Egypt": 0.21,
    "El Salvador": 0.63,
    "Equatorial Guinea": 0.54,
    "Eritrea": 0.95,
    "Estonia": 0.08,
    "Eswatini": 0.44,
    "Ethiopia": 0.30,
    "Fiji": 0.44,
    "Finland": 0.01,
    "France": 0.09,
    "Gabon": 0.68,
    "Gambia, The": 0.33,
    "Georgia": 0.17,
    "Germany": 0.06,
    "Ghana": 0.20,
    "Greece": 0.17,
    "Grenada": 0.57,
    "Guatemala": 0.69,
    "Guinea": 0.60,
    "Guinea-Bissau": 0.59,
    "Guyana": 0.57,
    "Haiti": 0.54,
    "Holy See (Vatican City State)": 0.96,
    "Honduras": 0.75,
    "Hungary": 0.19,
    "Iceland": 0.07,
    "India": 0.22,
    "Indonesia": 0.20,
    "Iran": 0.41,
    "Iraq": 0.67,
    "Ireland": 0.11,
    "Israel": 0.14,
    "Italy": 0.14,
    "Jamaica": 0.32,
    "Japan": 0.06,
    "Jordan": 0.24,
    "Kazakhstan": 0.23,
    "Kenya": 0.22,
    "Kiribati": 0.42,
    "North Korea": 0.68,
    "South Korea": 0.09,
    "Kuwait": 0.42,
    "Kyrgyz Republic": 0.57,
    "Laos": 0.47,
    "Latvia": 0.17,
    "Lebanon": 0.50,
    "Lesotho": 0.67,
    "Liberia": 0.77,
    "Libya": 0.61,
    "Liechtenstein": 0.30,
    "Lithuania": 0.12,
    "Luxembourg": 0.03,
    "Madagascar": 0.72,
    "Malawi": 0.40,
    "Malaysia": 0.15,
    "Maldives": 0.72,
    "Mali": 0.48,
    "Malta": 0.16,
    "Marshall Islands": 0.63,
    "Mauritania": 0.65,
    "Mauritius": 0.18,
    "Mexico": 0.30,
    "Micronesia, Fed. Sts.": 0.64,
    "Moldova": 0.32,
    "Monaco": 0.22,
    "Mongolia": 0.52,
    "Montenegro": 0.39,
    "Morocco": 0.21,
    "Mozambique": 0.36,
    "Myanmar": 0.38,
    "Namibia": 0.54,
    "Nauru": 0.62,
    "Nepal": 0.47,
    "Netherlands": 0.04,
    "New Zealand": 0.12,
    "Nicaragua": 0.82,
    "Niger": 0.63,
    "Nigeria": 0.43,
    "North Macedonia": 0.46,
    "Norway": 0.04,
    "Oman": 0.22,
    "Pakistan": 0.26,
    "Panama": 0.33,
    "Papua New Guinea": 0.52,
    "Paraguay": 0.48,
    "Peru": 0.28,
    "Philippines": 0.24,
    "Poland": 0.16,
    "Portugal": 0.15,
    "Qatar": 0.16,
    "Romania": 0.26,
    "Russian Federation": 0.62,
    "Rwanda": 0.21,
    "Samoa": 0.45,
    "San Marino": 0.47,
    "Sao Tome and Principe": 0.68,
    "Saudi Arabia": 0.20,
    "Senegal": 0.29,
    "Serbia": 0.20,
    "Seychelles": 0.26,
    "Sierra Leone": 0.38,
    "Singapore": 0.03,
    "Slovak Republic": 0.23,
    "Slovenia": 0.11,
    "Solomon Islands": 0.70,
    "Somalia": 0.81,
    "South Africa": 0.24,
    "South Sudan": 0.84,
    "Spain": 0.11,
    "Sri Lanka": 0.35,
    "St. Kitts and Nevis": 0.55,
    "St. Lucia": 0.56,
    "St. Vincent and the Grenadines": 0.55,
    "Sudan": 0.71,
    "Suriname": 0.62,
    "Sweden": 0.03,
    "Switzerland": 0.05,
    "Syrian Arab Republic": 0.49,
    "Tajikistan": 0.80,
    "Tanzania": 0.30,
    "Thailand": 0.19,
    "Timor-Leste": 0.74,
    "Togo": 0.25,
    "Tonga": 0.58,
    "Trinidad and Tobago": 0.52,
    "Tunisia": 0.25,
    "Turkiye": 0.22,
    "Turkmenistan": 0.81,
    "Tuvalu": 0.56,
    "Uganda": 0.29,
    "Ukraine": 0.50,
    "United Arab Emirates": 0.10,
    "United Kingdom": 0.11,
    "United States": 0.22,
    "Uruguay": 0.15,
    "Uzbekistan": 0.41,
    "Vanuatu": 0.40,
    "Venezuela, RB": 0.53,
    "Viet Nam": 0.20,
    "West Bank and Gaza": 0.66,
    "Yemen, Rep.": 0.94,
    "Zambia": 0.24,
    "Zimbabwe": 0.71
}

# Effort
REACHABILITY = {
    "Unknown": 0.50,
    "Air‑gapped / offline (physical access only)": 0.10,
    "Segregated VLAN (additional ACLs / jump hosts)": 0.30,
    "Internal network (requires VPN or lateral movement)": 0.50,
    "Partner / extranet (limited to trusted IP ranges)": 0.75,
    "Public internet (directly reachable)": 1.00,
}
LEGACY = {
    "Unknown": 0.50,
    "Fully current (supported and <30 days behind patches)": 0.25,
    "Modern but lagging (fully supported but >90 days behind patches)": 0.50,
    "Partial legacy (receives vendor ESU or limited back‑ports)": 0.75,
    "Critical legacy (OS/platform no longer receives patches)": 1.00,
}
SAFEGUARD = {
    "Unknown": 0.50,
    "Defence‑in‑depth: ≥3 layers + least‑privilege design": 0.20,
    "Moderate: 2 distinct safeguards (e.g., MFA + EDR)": 0.45,
    "Basic: 1 safeguard (e.g., MFA or EDR)": 0.70,
    "None: flat network (e.g., no MFA, no EDR)": 1.00,
}

# -----------------------------
# Actor weights (wI, wO)
# -----------------------------
ACTOR_WEIGHTS = {
    "NationState": (0.70, 0.30),
    "Cybercriminal": (0.20, 0.80),
    "IdeologyDriven": (0.50, 0.50),
    "MaliciousInsider": (0.30, 0.70),
}

# -----------------------------
# Helper: required selection wrapper
# -----------------------------

def select_required(label: str, mapping: dict, *, help_text: str | None = None):
    opts = ["-- Select --"] + list(mapping.keys())
    choice = st.selectbox(label, opts, index=0, help=help_text)
    if choice == "-- Select --":
        st.warning(f"Please choose a value")
        return None
    return mapping[choice]

def multiselect_required(label, options):
    selected = st.multiselect(label, options=options)
    if not selected:
        #st.error("Please select at least one option.")
        #st.stop()
        st.warning(f"Please choose a value")
        return None
    return selected

def capability_from_preset(preset_name: str) -> float:
    p = ACTOR_PRESETS[preset_name]
    s = SKILLS[p["SKILLS"]]
    c2 = RES_C2[p["RES_C2"]]
    z = RES_0DAY[p["RES_0DAY"]]
    t = TOOLING[p["TOOLING"]]
    tr = TRADECRAFT[p["TRADECRAFT"]]
    return (s + (c2 + z)/2 + t + tr) / 4.0

# -----------------------------
# UI – inputs
# -----------------------------
st.subheader("Inputs")
colA, colB, colC = st.columns(3)

# --- Attacker selection ---
with colA:
    st.markdown("**Attacker selection**")
    #capability_mode = st.radio(
    #    "Capability entry mode",
    #    ["Use actor preset", "Manual"],
    #    index=0,
    #    help="Preset fills Capability (C) automatically based on the chosen actor profile."
    #)
    primary_actor = st.selectbox(
        "Actor profile",
        list(ACTOR_WEIGHTS.keys()),
        index=1
    )
    C_preset = capability_from_preset(primary_actor)
    st.metric("Capability score C", f"{C_preset:.2f}")
    #st.markdown("**Capability**")
    #if capability_mode == "Use actor preset":
    #    C_preset = capability_from_preset(primary_actor)
    #    st.metric("Capability score C (preset)", f"{C_preset:.2f}")
    #    C = C_preset
    #else:
        # Manual required selects
        #v_skills = select_required("Skills breadth", SKILLS)
        #v_c2     = select_required("C2/botnet estate size", RES_C2)
        #v_0day   = select_required("Zero-day acquisition frequency", RES_0DAY)
        #v_tooling= select_required("Tooling & automation", TOOLING)
        #v_trade  = select_required("Operational tradecraft", TRADECRAFT)
        #C = (v_skills + (v_c2 + v_0day)/2 + v_tooling + v_trade) / 4

# -------------------
# Opportunity (colB)
# -------------------
with colB:
    st.markdown("**Opportunity**")
    v_apps   = select_required("Approx. internet-facing applications?", SURFACE_APPS)
    v_endp   = select_required("Approx. endpoints?", SURFACE_ENDPOINTS)
    v_social = select_required("Approx. employee count?", SOCIAL_SIZE)

# ---------------
# Intent (colC)
# ---------------
with colC:
    st.markdown("**Intent**")
    v_sector = select_required("Primary industry?", SECTOR)
    asset_help = (
        "Typical values for data records sold on the dark web:\n\n"
        "- Credit-card PAN+CVV: 8–12$ per record\n"
        "- Basic PII (name, address, email): 5–15$ per record\n"
        "- Full identity profiles (‘Fullz’): 20–100$ per profile\n"
        "- Medical records / EHR files: up to 500$ per record\n"
        "- IP/trade secrets: context-specific (often 10k$–M$+)\n"
        "- Government-restricted docs: context-specific (often $M+)"
    )
    v_asset  = select_required("Total monetary value of data held?", ASSET_VALUE, help_text=asset_help)
    v_crit   = select_required("Uptime / downtime tolerance?", CRITICALITY)

    selected_countries = st.multiselect(
        "Select operating countries (GeoRisk)",
        options=sorted(GEO_RISK.keys())
    )

# -----------------------
# Effort (always visible)
# -----------------------
st.markdown("**Effort (asset-specific)**")
colE1, colE2, colE3 = st.columns(3)
with colE1:
    v_reach = REACHABILITY[st.selectbox("How can an external attacker first reach the asset?", list(REACHABILITY.keys()))]
with colE2:
    v_legacy = LEGACY[st.selectbox("Does the system run unsupported or end-of-life components?", list(LEGACY.keys()))]
with colE3:
    v_safe   = SAFEGUARD[st.selectbox("How many independent defensive layers must be bypassed after initial access?", list(SAFEGUARD.keys()))]

# ----------------------------
# Validation gate (single spot)
# ----------------------------
errors = []
# Capability: if manual, ensure those selects are not None
#if capability_mode == "Manual":
#    if any(x is None for x in [v_skills, v_c2, v_0day, v_tooling, v_trade]):
#        errors.append("Please complete all Capability fields.\n")

# Opportunity & Intent required selects
if any(x is None for x in [v_apps, v_endp, v_social, v_sector, v_asset, v_crit]):
    errors.append("Please complete all Opportunity and Intent fields.\n")

# GeoRisk must have at least one country
if not selected_countries:
    errors.append("Please select at least one country for GeoRisk.")

if errors:
    st.warning("• " + "\n• ".join(errors))
    st.stop()

# ----------------------------
# Compute GeoRisk
# ----------------------------
vals = [GEO_RISK[c] for c in selected_countries]
georisk_score = max(vals)

st.write(f"**GeoRisk score**: {georisk_score:.3f}")

# Block compute until all required answers are chosen
#if capability_mode == "Manual":
#    required_answers = [v_skills, v_c2, v_0day, v_tooling, v_trade, v_apps, v_endp, v_social, v_sector, v_asset, v_crit]
#    if any(v is None for v in required_answers):
#        st.stop()
#else:
required_answers = [v_apps, v_endp, v_social, v_sector, v_asset, v_crit]
if any(v is None for v in required_answers):
    st.stop()

# -----------------------------
# Compute subscores
# -----------------------------
C = C_preset
O = ((v_apps + v_endp)/2 + v_social)/2
I = (v_sector + v_asset + v_crit + georisk_score) / 4
E = (v_reach + v_legacy + v_safe) / 3

st.divider()
st.subheader("Subscores (0–1)")
colS1, colS2, colS3, colS4 = st.columns(4)
colS1.metric("Capability C", f"{C:.2f}")
colS2.metric("Opportunity O", f"{O:.2f}")
colS3.metric("Intent I", f"{I:.2f}")
colS4.metric("Effort E", f"{E:.2f}")

# -----------------------------
# Results per actor
# -----------------------------
st.divider()
st.subheader(f"CTSS Results for {primary_actor}")

wI, wO = ACTOR_WEIGHTS[primary_actor]
base = ctss_calc(C, O, I, 0.5, wI, wO)
effort = ctss_calc(C, O, I, E, wI, wO)
st.write(f"**CTSSBase** (E=0.5): **{base:.3f}**")
st.write(f"**CTSSEffort**: **{effort:.3f}**")

#for actor, (wI, wO) in ACTOR_WEIGHTS.items():
#    base = ctss_calc(C, O, I, 0.5, wI, wO)
#    effort = ctss_calc(C, O, I, E, wI, wO)
#    st.write(f"{actor}")
#    st.write(f"**CTSSBase** (E=0.5): **{base:.3f}**  |  **CTSSEffort**: **{effort:.3f}**")
    #with st.expander(f"{actor}"):
    #    c1, c2, c3 = st.columns(3)
    #    c1.metric("wI", f"{wI:.2f}")
    #    c2.metric("wO", f"{wO:.2f}")
    #    st.write(f"**CTSSBase** (E=0.5): **{base:.3f}**  |  **CTSSEffort**: **{effort:.3f}**")
    #    st.progress(min(1.0, max(0.0, effort)))

st.info(
    """
    **Notes**
    - CTSSBase assumes unknown effort E=0.5. CTSSEffort uses your Effort inputs.
    - Select a value for every field in Capability, Opportunity, and Intent; Effort can stay Unknown.
    - For a full risk score, multiply CTSSEffort by normalized CVSS (CVSS/10).
    """
)
