import enum
import os
import logging
import random
from sys import stdout

import numpy as np
import pandas as pd
import streamlit as st
from numpy.random import Generator
from dotenv import load_dotenv

# Logging setup
logger = logging.getLogger('sorteggio corsia e piazzola')
logger.setLevel(logging.DEBUG)
logFormatter = logging.Formatter("%(name)-12s %(asctime)s %(levelname)-8s %(message)s")
consoleHandler = logging.StreamHandler(stdout)
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

logger.info("Logger setup")

st.set_page_config(page_title="Sorteggio kart e corsia", page_icon="🎲")

# Enum for Kart Drawer Status
class KartDrawerStatus(enum.Enum):
    STOP = 0
    RUNNING = 1

# Load environment variables
load_dotenv()
logger.info("Loaded .env")

# Default values
DEFAULT_NUMBER_KART = 15
num_karts = int(os.getenv("NUM_KART", DEFAULT_NUMBER_KART))
generator = np.random.default_rng()

# Initialize session state
if 'status' not in st.session_state:
    st.session_state.status = KartDrawerStatus.STOP.value
if 'drawn_karts_lanes' not in st.session_state:
    st.session_state.drawn_karts_lanes = pd.DataFrame({"Corsie Kart Sorteggiate": [], "Piazzole Kart Sorteggiate": []})

# Helper function to reset the DataFrame
def init_dataframe():
    return pd.DataFrame({"Corsie Kart Sorteggiate": []})

# Streamlit GUI
st.title("Sorteggio Numero e Corsia Kart")

# Number input for the number of karts
st.session_state.num_karts = st.number_input(
    "Seleziona il numero di kart da sorteggiare:",
    min_value=1, max_value=100,
    value=num_karts, step=1
)

if st.session_state.num_karts % 2 == 0:
    st.session_state.lanes_count: dict[str, int] = {
        "Bianca": st.session_state.num_karts // 2,
        "Rossa": st.session_state.num_karts // 2
    }
else:
    st.session_state.lanes_count: dict[str, int] = {
        "Bianca": st.session_state.num_karts // 2,
        "Rossa": st.session_state.num_karts // 2 + 1
    }

# Buttons layout
col1, col2, col3 = st.columns(3)

# Start Button
if col1.button("Start", disabled=st.session_state.status == KartDrawerStatus.RUNNING.value):
    st.session_state.status = KartDrawerStatus.RUNNING.value
    st.session_state.drawn_karts_lanes = init_dataframe()
    logger.info("Start button clicked")

# Draw Kart Button
if col2.button("Sorteggia", disabled=st.session_state.status == KartDrawerStatus.STOP.value):
    if len(st.session_state.drawn_karts_lanes) < st.session_state.num_karts:
        while True:
            drawn_kart = generator.integers(1, st.session_state.num_karts + 1)
            if drawn_kart not in st.session_state.drawn_karts_lanes["Piazzole Kart Sorteggiate"].values:
                while True:
                    drawn_lane: str = random.choice(["Bianca", "Rossa"])
                    if st.session_state.lanes_count.get(drawn_lane, 0) > 0:
                        st.session_state.lanes_count[drawn_lane] -= 1
                        break
            
                new_entry = pd.DataFrame({"Piazzole Kart Sorteggiate": [drawn_kart], "Corsie Kart Sorteggiate": [drawn_lane]})
                st.session_state.drawn_karts_lanes = pd.concat([st.session_state.drawn_karts_lanes, new_entry], ignore_index=True)
                st.session_state.drawn_kart_lane = (drawn_kart, drawn_lane)
                break
        logger.info(f"Kart {drawn_kart} - Lane {drawn_lane} drawn.")
    else:
        st.session_state.status = KartDrawerStatus.STOP.value

# Reset Button
if col3.button("Reset"):
    st.session_state.status = KartDrawerStatus.STOP.value
    st.session_state.drawn_karts_lanes = init_dataframe()
    logger.info("Reset button clicked")

# Display drawn kart
if 'drawn_kart_lane' in st.session_state:
    st.markdown(f"### Piazzola sorteggiata: {st.session_state.drawn_kart_lane[0]}. Corsia sorteggiata: {st.session_state.drawn_kart_lane[1]}")

st.session_state.drawn_karts_lanes.index += 1
# Display the DataFrame of drawn karts
st.dataframe(st.session_state.drawn_karts_lanes, width=700)

#st.run("sorteggio_piazzola.py", "--server.port=8501", "--server.address=0.0.0.0")
