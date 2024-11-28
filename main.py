import enum
import os
from typing import Final
import logging
from sys import stdout

import numpy as np
import pandas as pd
import taipy as tp
import taipy.gui.builder as tgb
from dotenv import load_dotenv
from numpy.random import Generator
from taipy.gui import Gui, State

logger = logging.getLogger('mylogger')

logger.setLevel(logging.DEBUG) # set logger level
logFormatter = logging.Formatter\
("%(name)-12s %(asctime)s %(levelname)-8s %(filename)s:%(funcName)s %(message)s")
consoleHandler = logging.StreamHandler(stdout) #set streamhandler to stdout
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

logger.info("Logger setup")

class KartDrawerStatus(enum.Enum):
    STOP: int = 0
    RUNNING: int = 1


load_dotenv()
logger.info("loaded dot env")

DEFAULT_NUMBER_KART: Final = 15
num_karts: int = os.getenv("NUM_KART", DEFAULT_NUMBER_KART)
drawn_kart: int | None = None
drawn_karts: pd.DataFrame = pd.DataFrame({"Piazzole Kart Sorteggiate": []})
status: bool = bool(KartDrawerStatus.STOP.value)
generator: Generator = np.random.default_rng()

logger.info("defined variables")

def init_dataframe() -> pd.DataFrame:
    return pd.DataFrame({"Piazzole Kart Sorteggiate": []})


def start(state: State) -> None:
    state.status = bool(KartDrawerStatus.RUNNING.value)
    state.drawn_karts = init_dataframe()


def reset(state: State) -> None:
    global generator
    generator = np.random.default_rng()

    state.status = bool(KartDrawerStatus.STOP.value)
    state.drawn_karts = init_dataframe()


def toggle_status(state: State) -> None:
    global generator
    state.status = not state.status

    # status = KartDrawerStatus.STOP if status == KartDrawerStatus.RUNNING else KartDrawerStatus.RUNNING
    generator = np.random.default_rng()


def set_num_karts(state: State) -> None:
    state.status = bool(KartDrawerStatus.STOP.value)
    state.drawn_karts = init_dataframe()


def draw_kart(state: State) -> None:
    if state.status == bool(KartDrawerStatus.STOP.value):
        return

    if state.drawn_karts.shape[0] == state.num_karts:
        state.status = bool(KartDrawerStatus.STOP.value)
        return

    while True:
        drawn_kart: int = generator.integers(low=1, high=state.num_karts + 1, size=None)
        if drawn_kart not in state.drawn_karts["Piazzole Kart Sorteggiate"].tolist():
            state.drawn_karts = pd.concat(
                [state.drawn_karts, pd.DataFrame(data={"Piazzole Kart Sorteggiate": [drawn_kart]})], axis=0
            )

            state.drawn_kart = drawn_kart

            if state.drawn_karts.shape[0] == state.num_karts:
                state.status = bool(KartDrawerStatus.STOP.value)
            return


if __name__ == "__main__":
    print("main")
    with tgb.Page() as page:
        tgb.text("# Sorteggio Piazzole Kart", mode="md")

        tgb.number(
            label="numero_kart",
            value="{num_karts}",
            hover_text="Seleziona il numero di piazzole kart da sorteggiare",
            on_change=set_num_karts,
            id="numero_kart_input",
        )

        with tgb.layout(columns="1 1 1") as layout:
            tgb.button(
                label="start",
                on_action=start,
                active="{not status}",
                id="start_button",
                hover_text="Inizia a sorteggiare le piazzole kart",
            )

            tgb.button(
                label="sorteggia",
                on_action=draw_kart,
                active="{status}",
                id="sorteggia_button",
                hover_text="Sorteggia la prossima piazzola kart",
            )

            tgb.button(
                label="reset",
                on_action=reset,
                active="{status}",
                id="reset_button",
                hover_text="Resetta sorteggio",
            )

        tgb.text(value="### Piazzola sorteggiata: {drawn_kart}", mode="md")

        tgb.table(data="{drawn_karts}", hover_text="Piazzole Kart gia' sorteggiate")

    gui = Gui(page)
    print("gui page created")
    app = tp.run(gui, title="Sorteggio Piazzole Kart", debug=True, port=5000, use_reloader=False, run_server=False)
    print("app run")
