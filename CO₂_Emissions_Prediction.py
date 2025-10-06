
import streamlit as st

# configure the page 
st.set_page_config(
    page_title="CO₂ Emissions Prediction",
    page_icon="🟢",
    layout="centered",
)


st.markdown(
    "<h1 style='text-align: center;'>CO₂ Emissions Prediction</h1>",
    unsafe_allow_html=True
)

st.markdown("---------------")

st.info("""
+ This web application allows the user to predict the CO₂ emissions from a ***fossil fuel*** driven power plant. 
+ The model predicting the emission values was created with measured emissions ***(not calculated)*** from power plants around the United States.

""")

st.markdown("---------------")


# load model
import pickle

loaded_model = pickle.load(open('model_pickle/trained_pipe_co2.sav', 'rb'))

# Inputs for the dropdown boxes:
fuel_code_options = {
    "BIT - Bituminous Coal": "BIT", "DFO - Distillate Fuel Oil": "DFO",
    "GEO - Geothermal": "GEO", "JF - Jet Fuel": "JF",
    "KER - Kerosene": "KER", "LIG - Lignite": "LIG",
    "MSW - Municipal Solid Waste": "MSW", "NG - Natural Gas": "NG",
    "PC - Petroleum Coke": "PC", "PG - Propane Gas": "PG",
    "RC - Refined Coal": "RC", "RFO - Residual Fuel Oil": "RFO",
    "SGC - Synthetic Gas from Coal": "SGC", "SUB - Subbituminous Coal": "SUB",
    "TDF - Tire-derived Fuel": "TDF", "WC - Waste Coal": "WC",
    "WO - Waste/Used Oil": "WO"
}
prime_mover_options = {
    "CA - Combined Cycle (Multi-Shaft)": "CA", "CE - Compressed Air Energy Storage": "CE",
    "CS - Compressed Air Storage": "CS", "CT - Combined Cycle (Single Shaft)": "CT",
    "FC - Fuel Cell": "FC", "GT - Combustion Turbine (Gas Turbine)": "GT",
    "IC - Internal Combustion Engine": "IC", "OT - Other": "OT",
    "ST - Steam Turbine": "ST"
}


# Initialize session defaults

if 'FuComElGen' not in st.session_state: st.session_state.FuComElGen = 0.0
if 'ToFuCom' not in st.session_state: st.session_state.ToFuCom = 0.0
if 'Gen' not in st.session_state: st.session_state.Gen = 0.0
if "FuCod" not in st.session_state: st.session_state.FuCod = list(fuel_code_options.keys())[0]
if 'PriMov' not in st.session_state: st.session_state.PriMov = list(prime_mover_options.keys())[0]

# Use the st.session_state values in the widgets

FuComElGen = st.number_input('Fuel Consumption for Electric Generation (MMBtu)', value=st.session_state.FuComElGen)
ToFuCom = st.number_input('Total Fuel Consumption (MMBtu)', value=st.session_state.ToFuCom)
Gen = st.number_input('Generation (kWh)', value= st.session_state.Gen)
FuCod = st.selectbox("Fuel Code", list(fuel_code_options.keys()), index=list(fuel_code_options.keys()).index(st.session_state.FuCod))
PriMov = st.selectbox('Prime Mover', list(prime_mover_options.keys()), index=list(prime_mover_options.keys()).index(st.session_state.PriMov))

# Update session state after input

st.session_state.FuComElGen = FuComElGen
st.session_state.ToFuCom = ToFuCom
st.session_state.Gen = Gen
st.session_state.FuCod = FuCod
st.session_state.PriMov = PriMov


# new plant input DataFrame
import pandas as pd
new_plant = pd.DataFrame({
    'Fuel Consumption for Electric Generation (MMBtu)':[FuComElGen],
    'Total Fuel Consumption (MMBtu)':[ToFuCom],
    'Generation (kWh)':[Gen],
    'Fuel Code':[fuel_code_options[FuCod]],
    'Prime Mover':[prime_mover_options[PriMov]]
})

# predictict and store in session_state
if st.button("Predict CO2 Emissions"):
    co2_prediction = loaded_model.predict(new_plant)[0] #Extract scalar from array
    st.session_state.co2_prediction = co2_prediction
    st.success(f"The estimated CO2 emission for your plant are: {co2_prediction: .2f} Ton/year")

st.markdown("<div style='text-align: right'><strong> Data source for modelling:</strong> https://www.eia.gov/electricity/data </div>",
            unsafe_allow_html=True
)
