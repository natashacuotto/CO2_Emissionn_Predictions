
import streamlit as st
import pandas as pd
import pickle

# configure the page 
st.set_page_config(
    page_title="Standards & Strategy: Details",
    page_icon="ℹ️",
    layout="centered",
)

# Title
st.title("Emissions Standards and Strategy - Details")
st.markdown("")
st.success("**Find detailed information here about content presented on page 2**")

# Diccionarios ordenados alfabéticamente

boiler_status = {
    "CN": "Cancelled (previously reported as 'planned')",
    "CO": "New unit under construction",
    "OP": "Operating (in commercial service or out of service < 365 days)",
    "OS": "Out of service (365 days or longer)",
    "PL": "Planned (expected to go into service within 10 years)",
    "RE": "Retired",
    "SB": "Standby (inactive reserve)",
    "SC": "Cold Standby (requires 3 to 6 months to reactivate)",
    "TS": "Operating under test conditions"
}

type_boilers = {
    "D":  "Standards of Performance for fossil-fuel fired steam boilers for which construction began after August 17, 1971.",
    "Da": "Standards of Performance for fossil-fuel fired steam boilers for which construction began after September 18, 1978.",
    "Db": "Standards of Performance for fossil-fuel fired steam boilers for which construction began after June 19, 1984.",
    "Dc": "Standards of Performance for small industrial-commercial-institutional steam generating units.",
    "N":  "Not covered under New Source Performance Standards."
}

regulation_sulfur_nitrogen_particulate = {"FD": "Federal",
"ST" : "State level",
"LO": "Local",
'XX': "Unvavailable or Unknown"}

so2_control_strategy_1 = {
    "CF": "Fluidized Bed Combustor",
    "IF": "Use flue gas desulfurization unit or other SO₂ control process",
    "NA": "Not applicable",
    "ND": "Not determined at this time",
    "NP": "No plans to control",
    "OT": "Other (specify in Schedule 7)",
    "SE": "Seeking revision of government regulation",
    "SS": "Switch to lower sulfur fuel",
    "WA": "Allocated allowances and purchase allowances"
}

nox_control_strategy_1 = {
    "AA": "Advanced overfire air",
    "BF": "Biased firing (alternative burners)",
    "BO": "Burner out of service",
    "CF": "Fluidized bed combustor",
    "FR": "Flue gas recirculation",
    "FU": "Fuel reburning",
    "H2O": "Water injection",
    "LA": "Low excess air",
    "LN": "Low NOx burner",
    "MS": "Currently meeting standard",
    "NA": "Not applicable",
    "NC": "No change in historic operation of unit anticipated",
    "ND": "Not determined at this time",
    "NH3": "Ammonia injection",
    "NP": "No plans to control",
    "OT": "Other (unspecified or see Schedule 7)",
    "OV": "Overfire air",
    "RP": "Repower unit",
    "SC": "Slagging",
    "SE": "Seeking revision of government regulation",
    "SN": "Selective noncatalytic reduction (SNCR)",
    "SR": "Selective catalytic reduction (SCR)",
    "STM": "Steam injection",
    "UE": "Decrease utilization – rely on energy conservation and/or improved efficiency"
}

mercury_control_strategy_1 = {
    "ACI": "Activated carbon injection system",
    "BP": "Baghouse (fabric filter), pulse",
    "BR": "Baghouse (fabric filter), reverse air",
    "BS": "Baghouse (fabric filter), shake and deflate",
    "CD": "Circulating dry scrubber",
    "DSI": "Dry sorbent (powder) injection type",
    "EC": "Electrostatic precipitator, cold side, with flue gas conditioning",
    "EH": "Electrostatic precipitator, hot side, with flue gas conditioning",
    "EK": "Electrostatic precipitator, cold side, without flue gas conditioning",
    "EW": "Electrostatic precipitator, hot side, without flue gas conditioning",
    "FP": "Fabric filter with powdered activated carbon",
    "HGP": "High gradient magnetic separation",
    "JB": "Jet bubbling reactor (wet) scrubber",
    "LIJ": "Lime injection",
    "MA": "Mechanically aided type (wet) scrubber",
    "MS": "Currently meeting standard",
    "MW": "Mercury wet scrubber",
    "NA": "Not applicable",
    "ND": "Not determined at this time",
    "OT": "Other (specify in SCHEDULE 7)",
    "PA": "Packed type (wet) scrubber",
    "RA": "Regenerative activated coke technology",
    "RB": "Rotating belt filter",
    "SD": "Spray dryer type / dry FGD / semi-dry FGD",
    "SP": "Spray type (wet) scrubber",
    "TR": "Tray type (wet) scrubber",
    "VE": "Venturi type (wet) scrubber"
}

steam_plant_type = {
    1: "Plants with combustible-fueled steam-electric generators ≥ 100 MW capacity (including combined cycle steam-electric with duct firing).",
    2: "Plants with combustible-fueled steam-electric generators ≥ 10 MW but < 100 MW capacity (including combined cycle steam-electric with duct firing).",
    3: "Plants with nuclear fueled, combined cycle steam-electric without duct firing, solar thermal electric with steam cycle ≥ 100 MW.",
    4: "Plants with non-steam fueled electric generators (wind, PV, geothermal, fuel cell, combustion turbines, IC engines, etc.)."
}

additional_info = {
    "State": "United States of America states where the plant is located.",
    "Boiler ID": "Unique identifier of boilers within a plant."
}

# Read from Pickle the emissions strategy information

try:
    with open("model_pickle/emiss_strategy_plant.pkl", "rb") as f:
        emiss_strategy_plant = pickle.load(f)
except Exception as e:
    st.error(f"Error loading emissions-strategy data: {e}")
    st.stop()

selected_plant = st.session_state.get("selected_plant", None)
if selected_plant is None:
    st.warning("No plant selected yet. Please go to Page 2 first.")
    st.stop()

# Ensure column is int
emiss_strategy_plant["Plant Code"] = emiss_strategy_plant["Plant Code"].astype(int)
plant_data = emiss_strategy_plant[emiss_strategy_plant["Plant Code"] == selected_plant]

if plant_data.empty:
    st.warning("No data found for selected plant.")
    st.stop()

plant_name = plant_data["Plant Name"].iloc[0]

# Mostrar valores destacados si existen en sesión
highlight_plant = st.session_state.get("selected_plant", None)
highlight_co2 = st.session_state.get("co2_prediction", None)

st.markdown("---")

if highlight_plant is not None:
    st.info(f"🟢 Selected Plant Code - Plant Name: **{highlight_plant} - {plant_name}**")
if highlight_co2 is not None:
    st.info(f"🔵 CO₂ predicted emissions: **{highlight_co2:,.0f}Ton**")


# --- Show actual decoded values from selected plant ---
st.markdown("---")
st.subheader("📌 Standars & Strategy Values for Selected Plant")


# Get the first row
#plant_row = plant_data.iloc[0]


# Fields and dictionaries to decode
decode_map = {
    "Boiler Status": boiler_status,
    "Type of Boiler": type_boilers,
    "Regulation Sulfur": regulation_sulfur_nitrogen_particulate,
    "Sulfur Dioxide Control Existing Strategy 1": so2_control_strategy_1,
    "Sulfur Dioxide Control Proposed Strategy 1": so2_control_strategy_1,
    "Regulation Nitrogen": regulation_sulfur_nitrogen_particulate,
    "Nitrogen Oxide Control Existing Strategy 1": nox_control_strategy_1,
    "Nitrogen Oxide Control Proposed Strategy 1": nox_control_strategy_1,
    "Regulation Particulate": regulation_sulfur_nitrogen_particulate,
    "Regulation Mercury": regulation_sulfur_nitrogen_particulate,
    "Mercury Control Existing Strategy 1": mercury_control_strategy_1,
    "Mercury Control Proposed Strategy 1": mercury_control_strategy_1,
    "Steam Plant Type": steam_plant_type
}

# Table
# Table all info together

comparison_rows = []
row_labels = []

for field in decode_map:
    row = {}
    for _, boiler in plant_data.iterrows():
        raw_val = boiler.get(field, "NA")
        if pd.isna(raw_val) or raw_val == "":
            raw_val = "NA"
            meaning = "Not Available"
        else:
            meaning = decode_map[field].get(raw_val, "Unknown")
        boiler_label = f"Boiler ID: {boiler['Boiler ID']}"
        row[boiler_label] = f"{raw_val} – {meaning}"
    comparison_rows.append(row)
    row_labels.append(field)

# DataFrame
comparison_df = pd.DataFrame(comparison_rows, index=row_labels)
comparison_df.index.name = "Emissions Standars & Strategy"
# Show the table
#st.markdown("Each column below represents a boiler identified by its unique **Boiler ID**, from the previous results.")

#st.dataframe(comparison_df, use_container_width=True)



# Show list dropdown menu per boilder:
st.markdown("###  Boiler Comparison by ID")
for col in comparison_df.columns:
    with st.expander(f"ℹ️ Details for {col}"):
        for index, value in comparison_df[col].items():
            st.markdown(f"**{index}**: {value}")


# Legend

st.markdown("---")
st.subheader("📚 List of codes")



# Función para imprimir diccionarios ordenados
def print_dict(title, dictionary):
    st.subheader(title)
    for key, val in sorted(dictionary.items()):
        st.markdown(f"- `{key}`: {val}")

# Expanders para cada bloque de códigos
with st.expander("🔥 Boiler Status - Codes"):
    print_dict("", boiler_status)

with st.expander("🔥 Types of Boilers"):
    print_dict("", type_boilers)

with st.expander("🔥 Emission Regulation - Codes"):
    print_dict("", regulation_sulfur_nitrogen_particulate)

with st.expander("🔥 SO₂ Control Strategy 1 - Codes"):
    print_dict("", so2_control_strategy_1)

with st.expander("🔥 NOx Control Strategy 1 - Codes"):
    print_dict("", nox_control_strategy_1)

with st.expander("🔥 Mercury Control Strategy 1 - Codes"):
    print_dict("", mercury_control_strategy_1)

with st.expander("🔥 Steam Plant Types"):
    print_dict("", steam_plant_type)

st.markdown("---")
st.subheader("ℹ️ Aditional Information")
for key, val in additional_info.items():
    st.markdown(f"- **{key}**: {val}")
