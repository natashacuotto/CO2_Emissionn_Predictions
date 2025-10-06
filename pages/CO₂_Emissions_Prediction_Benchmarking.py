

import streamlit as st
import pandas as pd
import pickle

# configure the page 
st.set_page_config(
    page_title="CO₂ Emissions Prediction Benchmarking",
    page_icon="📌",
    layout="centered",
)

# st.title("CO₂ Emissions and Power Generation Comparison")
st.markdown(
    "<h1 style='text-align: center;'>CO₂ Emissions and Generation Comparison</h1>",
    unsafe_allow_html=True
)


# Step 1: Retrieve prediction from session state
co2_prediction = st.session_state.get("co2_prediction", None)
if co2_prediction is None:
    st.warning("No CO₂ prediction found. Please run Page 1 first.")
    st.stop()

st.markdown("---------------")
st.write(f"Using predicted CO₂ emissions:  **{co2_prediction:,.0f} Ton**")

# Retrieve Generation entered for the plant to predict emissions from page 1 (session state)
gen_plant = st.session_state.get("Gen", None)
if gen_plant is None:
    st.warning("Generation input (kWh) is missing. Please start with Page 1.")
    st.stop()

st.write(f"Using an input plant generation of:  **{gen_plant:,.0f} kWh**")

st.markdown("---------------")
# Step 2: load emissions data and Plant Generation from Pickle

try: 
    with open("model_pickle/emissions.pkl", "rb") as f:
        co2emissions_plant = pickle.load(f)
except Exception as e:
    st.error (f"Error loading emissions data: {e}")
    st.stop()

# Initialize session state for slider
if "range_percent_emiss" not in st.session_state:
    st.session_state.range_percent_emiss = 10

# Sidebar slider for dynamic range to filter similar emissions
range_percent_emiss = st.sidebar.slider(
    "Select ± range around predicted CO₂ emissions",
    min_value=1,
    max_value=25,
    value=st.session_state.range_percent_emiss,
    step=1,
    help="Adjust the percentage range to filter similar emissions"
)
# Update session state for slider
st.session_state.range_percent_emiss = range_percent_emiss

# Calculate bounds: emissions
lower_bound = co2_prediction * (1 - range_percent_emiss / 100)
upper_bound = co2_prediction * (1 + range_percent_emiss / 100)



# Filter data with error handling. Emissions.
try:
    filtered_co2_emissions = co2emissions_plant[
        (co2emissions_plant["Tons of CO2 Emissions"] >= lower_bound) &
        (co2emissions_plant["Tons of CO2 Emissions"] <= upper_bound)
    ][["Plant Code", "Tons of CO2 Emissions", "Generation (kWh)"]]
except KeyError:
    st.error("Data must contain the 'Plant Code', 'Tons of CO₂ Emissions' and 'Generation (kWh)' columns.")
    st.stop()



# Display the bar charts: Emissions
import plotly.graph_objects as go

if filtered_co2_emissions.empty:
    st.warning(f"No plants found within (±{range_percent_emiss}%) of predicted emissions.")
else:
    # Add predicted value as a syntetic row
    plot_df = filtered_co2_emissions.copy()
    predicted_row = pd.DataFrame({
        "Plant Code": ["Predicted Value"],
        "Tons of CO2 Emissions": [co2_prediction],
        "Generation (kWh)":[gen_plant]
    })
    plot_df = pd.concat([plot_df, predicted_row], ignore_index = True)
    
    plot_df = plot_df.sort_values("Tons of CO2 Emissions").reset_index(drop=True)

    # Assign colors:

    colors_emiss = ["steelblue" if code == "Predicted Value" else "skyblue" for code in plot_df["Plant Code"]]
    
    colors_gen = ["indianred" if code == "Predicted Value" else "rosybrown" for code in plot_df["Plant Code"]]
        
 
    # Create the figure
    fig_dual = go.Figure()

    # Primary Y-axis: Tons of CO2 Emissions
    fig_dual.add_trace(go.Bar(
        x=plot_df['Plant Code'],
        y=plot_df['Tons of CO2 Emissions'],
        name='CO₂ Emissions (Ton)',
        marker_color=colors_emiss,
        yaxis='y1'
    ))

    # Secondary Y-axis: Generation (kWh)
    fig_dual.add_trace(go.Bar(
        x=plot_df['Plant Code'],
        y=plot_df['Generation (kWh)'],
        name='Generation (kWh)',
        marker_color=colors_gen,
        yaxis='y2'
    ))

    # Update layout for dual axes
    fig_dual.update_layout(
        title='CO₂ Emissions vs Generation by Plant',
        xaxis=dict(
            title='Plant Code',
            type='category'
        ),
        yaxis=dict(
            title='CO₂ Emissions (Ton)',
            titlefont=dict(color="steelblue"),
            tickfont=dict(color="steelblue"),
            # titlefont=dict(color=colors_emiss[0]), # hier assigns the series color to the font
            # tickfont=dict(color=colors_emiss[0])
        ),
        yaxis2=dict(
            title='Generation (kWh)',
            titlefont=dict(color='indianred'),
            tickfont=dict(color='indianred'),
            overlaying='y',
            side='right'
        ),
        legend=dict(x=0.01, y=0.99),
        barmode='group',
        margin=dict(l=40, r=40, t=60, b=40)
    )

    # Display in Streamlit
    st.plotly_chart(fig_dual, use_container_width=True)


# Dropdown menu 1. Have only Plant Codes from filtered_co2_emissions:

emiss_codes = filtered_co2_emissions["Plant Code"].drop_duplicates().sort_values()

# Ensure it's a list (Streamlit prefers lists over Series)
emiss_codes_list = emiss_codes.tolist()

# Initialize session state with first value if not set
if "selected_plant" not in st.session_state:
    if emiss_codes_list: # Make sure it's not empty
        st.session_state.selected_plant = emiss_codes_list[0] 
    else:
        st.warning("No plant codes available.")
        st.stop()

# Find index of current selction safely
try:
    index =emiss_codes_list.index(st.session_state.selected_plant)
except ValueError:
    index=0  # Fallback if not found



# Create dropdown
selected_plant = st.selectbox(
    "Select a Plant Code of interest to Access its Emissions Standards and Strategies",
    emiss_codes_list,
    index=index
)

# Update session state
st.session_state.selected_plant = selected_plant


# Load the emissions-strategy data from Pickle

try:
    with open("model_pickle/emiss_strategy_plant.pkl", "rb") as f:
        emiss_strategy_plant = pickle.load(f)
except Exception as e:
    st.error(f"Error loading emissions-strategy data: {e}")
    st.stop()

# Filter emissions-strategy data based on selecte_plant

st.write(f"You selected: **{selected_plant}**")
# st.write(f"Type of emiss_strategy_plant: {type(emiss_strategy_plant)}") # It was used to control the type of file emiss_strategy_plant is.



# Filter metadata for selected plant

selected_plant = int(selected_plant)
emiss_strategy_plant["Plant Code"]= emiss_strategy_plant["Plant Code"].astype(int)
co2emissions_plant["Plant Code"] = co2emissions_plant["Plant Code"].astype(int)  #Added 01.10.25 16:00

# Filter emissions strategy:
matching_rows = emiss_strategy_plant[emiss_strategy_plant["Plant Code"] == selected_plant]
matching_rows = matching_rows.reset_index() # Bring index into a column
matching_rows = matching_rows.drop(columns=["index"]) # removes that column... It is not reflected on the plot... this step is not necessary 

# Filer Prime Mover and Fuel Code:
matching_rows_mover = co2emissions_plant[co2emissions_plant["Plant Code"] == selected_plant]
matching_rows_mover = matching_rows_mover.reset_index() # Bring index into a column
matching_rows_mover = matching_rows_mover[["Plant Code", "Prime Mover", "Fuel Code"]]

# Df for strategy
if matching_rows.empty:
    st.warning("No metadata found for the selected Plant Code.")
else:
    st.subheader("Plant Emissions-Strategy Data")
    st.dataframe(matching_rows, use_container_width=True)

# Df for Mover
if matching_rows_mover.empty:
    st.warning("No metadata found for the selected Plant Code.")
else:
    st.subheader("Selected plant Prime Mover and Fuel")
    st.dataframe(matching_rows_mover, use_container_width=True)


