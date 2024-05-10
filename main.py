import enum
import os
from typing import Final

import numpy as np
import pandas as pd
import taipy as tp
import taipy.gui.builder as tgb
from dotenv import load_dotenv
from numpy.random import Generator
from taipy.gui import Gui, State

load_dotenv()


class KartDrawerStatus(enum.Enum):
    STOP: int = 0
    RUNNING: int = 1


DEFAULT_NUMBER_KART: Final = 15
num_karts: int = os.getenv("NUM_KART", DEFAULT_NUMBER_KART)
drawn_karts: pd.DataFrame = pd.DataFrame(data={"kart_sorteggiati": []})
status: bool = bool(KartDrawerStatus.STOP.value)
generator: Generator = np.random.default_rng()


def start(state: State, id: str | None) -> None:
    print(f"old start status = {state.status}")
    state.status = bool(KartDrawerStatus.RUNNING.value)
    state.drawn_karts = pd.DataFrame({"kart_sorteggiati": []})
    print(f"new start status = {state.status}")


def reset(state: State, id: str | None) -> None:
    global generator
    print(f"old reset status = {state.status}")
    state.status = bool(KartDrawerStatus.STOP.value)
    print(f"new reset status = {state.status}")
    generator = np.random.default_rng()
    state.drawn_karts = pd.DataFrame({"kart_sorteggiati": []})


def toggle_status(state: State, id: str | None, payload: dict[str, str | list]) -> None:
    global status
    state.status = not state.status

    # status = KartDrawerStatus.STOP if status == KartDrawerStatus.RUNNING else KartDrawerStatus.RUNNING
    generator = np.random.default_rng()


def set_num_karts(state: State, id: str | None, payload: dict[str, str | list]) -> None:
    print("\n\nnum kart setter")
    print(f"payload = {payload}")

    state.status = bool(KartDrawerStatus.STOP.value)
    state.drawn_karts = pd.DataFrame({"kart_sorteggiati": []})


def draw_kart(state: State, id: str | None, payload: dict) -> None:
    print(f"state.num_karts: {state.num_karts}. drawn_kart shape: {state.drawn_karts.shape}")
    if state.num_karts == KartDrawerStatus.STOP or state.drawn_karts.shape[0] == state.num_karts:
        state.status = KartDrawerStatus.STOP
        return

    while True:
        drawn_kart: int = generator.integers(low=1, high=state.num_karts + 1, size=None)
        if drawn_kart not in state.drawn_karts.kart_sorteggiati.tolist():
            state.drawn_karts = pd.concat(
                [state.drawn_karts, pd.DataFrame(data={"kart_sorteggiati": [drawn_kart]})], axis=0
            )

            if state.drawn_karts.shape[0] == state.num_karts:
                state.status = bool(KartDrawerStatus.STOP.value)
            return


with tgb.Page() as page:
    tgb.text("# Sorteggio Kart", mode="md")

    tgb.number(
        label="numero_kart",
        value="{num_karts}",
        hover_text="Seleziona il numero di kart da sorteggiare",
        on_change=set_num_karts,
        # on_action=set_num_karts,
        id="numero_kart_input",
    )

    with tgb.layout(columns="1 1 1") as layout:
        tgb.button(
            label="start",
            on_action=start,
            active="{not status}",
            id="start_button",
            hover_text="Inizia a sorteggiare i kart",
            # properties={"status": status},
        )

        tgb.button(
            label="sorteggia",
            on_action=draw_kart,
            active="{status}",
            id="sorteggia_button",
            hover_text="Inizia a sorteggiare i kart",
        )

        tgb.button(
            label="reset",
            on_action=reset,
            active="{status}",
            id="reset_button",
            hover_text="Resetta sorteggio",
        )

    tgb.table(data="{drawn_karts}", hover_text="Kart gia' sorteggiati")

gui = Gui(page)
app = tp.run(gui, title="Sorteggio Kart", debug=False, use_reloader=False, run_server=False)
